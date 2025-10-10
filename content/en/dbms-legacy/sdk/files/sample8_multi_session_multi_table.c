#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <pthread.h>
#include <machbase_sqlcli.h>
 
#define MACHBASE_PORT_NO       5656
#define ERROR_CHECK_COUNT   100
 
#define LOG_FILE_CNT        3
#define MAX_THREAD_NUM      LOG_FILE_CNT
 
#define RC_FAILURE          -1
#define RC_SUCCESS          0
 
#define UNUSED(aVar) do { (void)(aVar); } while(0)
 
char *gTableName[LOG_FILE_CNT] = {"table_f1", "table_f2", "table_event"};
char *gFileName[LOG_FILE_CNT] =  {"suffle_data1.txt","suffle_data2.txt","suffle_data3.txt"};
 
void printError(SQLHENV aEnv, SQLHDBC aCon, SQLHSTMT aStmt, char *aMsg);
int connectDB(SQLHENV *aEnv, SQLHDBC *aCon);
void disconnectDB(SQLHENV aEnv, SQLHDBC aCon);
int executeDirectSQL(SQLHENV aEnv, SQLHDBC aCon, const char *aSQL, int aErrIgnore);
int appendOpen(SQLHENV aEnv, SQLHDBC aCon, SQLHSTMT aStmt, char* aTableName);
int appendClose(SQLHENV aEnv, SQLHDBC aCon, SQLHSTMT aStmt);
int createTables(SQLHENV aEnv, SQLHDBC aCon);
 
/*
 * error code returned from CLI lib
 */
void printError(SQLHENV aEnv, SQLHDBC aCon, SQLHSTMT aStmt, char *aMsg)
{
    SQLINTEGER      sNativeError;
    SQLCHAR         sErrorMsg[SQL_MAX_MESSAGE_LENGTH + 1];
    SQLCHAR         sSqlState[SQL_SQLSTATE_SIZE + 1];
    SQLSMALLINT     sMsgLength;
 
    if( aMsg != NULL )
    {
        printf("%s\n", aMsg);
    }
 
    if( SQLError(aEnv, aCon, aStmt, sSqlState, &sNativeError,
                 sErrorMsg, SQL_MAX_MESSAGE_LENGTH, &sMsgLength) == SQL_SUCCESS )
    {
        printf("SQLSTATE-[%s], Machbase-[%d][%s]\n", sSqlState, sNativeError, sErrorMsg);
    }
}
 
/*
 * error code returned from Machbase server
 */
 
void appendDumpError(SQLHSTMT    aStmt,
                     SQLINTEGER  aErrorCode,
                     SQLPOINTER  aErrorMessage,
                     SQLLEN      aErrorBufLen,
                     SQLPOINTER  aRowBuf,
                     SQLLEN      aRowBufLen)
{
    char       sErrMsg[1024] = {0, };
    char       sRowMsg[32 * 1024] = {0, };
 
    UNUSED(aStmt);
 
    if (aErrorMessage != NULL)
    {
        strncpy(sErrMsg, (char *)aErrorMessage, aErrorBufLen);
    }
 
    if (aRowBuf != NULL)
    {
        strncpy(sRowMsg, (char *)aRowBuf, aRowBufLen);
    }
 
    fprintf(stdout, "Append Error : [%d][%s]\n[%s]\n\n", aErrorCode, sErrMsg, sRowMsg);
}
 
 
int connectDB(SQLHENV *aEnv, SQLHDBC *aCon)
{
    char sConnStr[1024];
 
    if( SQLAllocEnv(aEnv) != SQL_SUCCESS )
    {
        printf("SQLAllocEnv error\n");
        return RC_FAILURE;
    }
 
    if( SQLAllocConnect(*aEnv, aCon) != SQL_SUCCESS )
    {
        printf("SQLAllocConnect error\n");
 
        SQLFreeEnv(*aEnv);
        *aEnv = SQL_NULL_HENV;
 
        return RC_FAILURE;
    }
 
    sprintf(sConnStr,"SERVER=127.0.0.1;UID=SYS;PWD=MANAGER;CONNTYPE=1;PORT_NO=%d", MACHBASE_PORT_NO);
 
    if( SQLDriverConnect( *aCon, NULL,
                          (SQLCHAR *)sConnStr,
                          SQL_NTS,
                          NULL, 0, NULL,
                          SQL_DRIVER_NOPROMPT ) != SQL_SUCCESS
      )
    {
 
        printError(*aEnv, *aCon, NULL, "SQLDriverConnect error");
 
        SQLFreeConnect(*aCon);
        *aCon = SQL_NULL_HDBC;
 
        SQLFreeEnv(*aEnv);
        *aEnv = SQL_NULL_HENV;
 
        return RC_FAILURE;
    }
 
    return RC_SUCCESS;
}
 
 
void disconnectDB(SQLHENV aEnv, SQLHDBC aCon)
{
    if( SQLDisconnect(aCon) != SQL_SUCCESS )
    {
        printError(aEnv, aCon, NULL, "SQLDisconnect error");
    }
 
    SQLFreeConnect(aCon);
    aCon = SQL_NULL_HDBC;
 
    SQLFreeEnv(aEnv);
    aEnv = SQL_NULL_HENV;
}
 
 
int executeDirectSQL(SQLHENV aEnv, SQLHDBC aCon, const char *aSQL, int aErrIgnore)
{
    SQLHSTMT sStmt = SQL_NULL_HSTMT;
 
    if( SQLAllocStmt(aCon, &sStmt) != SQL_SUCCESS )
    {
        if( aErrIgnore == 0 )
        {
            printError(aEnv, aCon, sStmt, "SQLAllocStmt Error");
            return RC_FAILURE;
        }
    }
 
    if( SQLExecDirect(sStmt, (SQLCHAR *)aSQL, SQL_NTS) != SQL_SUCCESS )
    {
 
        if( aErrIgnore == 0 )
        {
            printError(aEnv, aCon, sStmt, "SQLExecDirect Error");
 
            SQLFreeStmt(sStmt,SQL_DROP);
            sStmt = SQL_NULL_HSTMT;
            return RC_FAILURE;
        }
    }
 
    if( SQLFreeStmt(sStmt, SQL_DROP) != SQL_SUCCESS )
    {
        if (aErrIgnore == 0)
        {
            printError(aEnv, aCon, sStmt, "SQLFreeStmt Error");
            sStmt = SQL_NULL_HSTMT;
            return RC_FAILURE;
        }
    }
    sStmt = SQL_NULL_HSTMT;
 
    return RC_SUCCESS;
}
 
 
int appendOpen(SQLHENV aEnv, SQLHDBC aCon, SQLHSTMT aStmt, char* aTableName)
{
    if( aTableName == NULL )
    {
        printf("append open wrong table name");
        return RC_FAILURE;
    }
 
    if( SQLAppendOpen(aStmt, (SQLCHAR *)aTableName, ERROR_CHECK_COUNT) != SQL_SUCCESS )
    {
        printError(aEnv, aCon, aStmt, "SQLAppendOpen error");
        return RC_FAILURE;
    }
    return RC_SUCCESS;
}
 
 
int appendClose(SQLHENV aEnv, SQLHDBC aCon, SQLHSTMT aStmt)
{
    int sSuccessCount = 0;
    int sFailureCount = 0;
 
    if( SQLAppendClose(aStmt, &sSuccessCount, &sFailureCount) != SQL_SUCCESS )
    {
        printError(aEnv, aCon, aStmt, "SQLAppendClose error");
        return RC_FAILURE;
    }
 
    printf("append result success : %d, failure : %d\n", sSuccessCount, sFailureCount);
 
    return RC_SUCCESS;
}
 
 
int createTables(SQLHENV aEnv, SQLHDBC aCon)
{
    int      i;
    char    *sSchema[] = { "srcip1 ipv4, srcip2 ipv6, srcport short, dstip1 ipv4, dstip2 ipv6, dstport short, data1 long, data2 long",
        "srcip1 ipv4, srcip2 ipv6, srcport short, dstip1 ipv4, dstip2 ipv6, dstport short, data1 long, data2 long",
        "machine ipv4, err integer, msg varchar(30)"
    };
 
    char sDropQuery[256];
    char sCreateQuery[256];
 
    for(i = 0; i < LOG_FILE_CNT; i++)
    {
        snprintf(sDropQuery, 256, "DROP TABLE %s", gTableName[i]);
        snprintf(sCreateQuery, 256, "CREATE TABLE %s ( %s )", gTableName[i], sSchema[i]);
 
        executeDirectSQL(aEnv, aCon, sDropQuery, 1);
        executeDirectSQL(aEnv, aCon, sCreateQuery, 0);
    }
 
    return RC_SUCCESS;
}
 
 
int appendF1(SQLHENV aEnv, SQLHDBC aCon, SQLHSTMT aStmt, FILE *aFp)
{
    SQL_APPEND_PARAM sParam[8];
    SQLRETURN        sRC;
 
    SQLINTEGER      sNativeError;
    SQLCHAR         sErrorMsg[SQL_MAX_MESSAGE_LENGTH + 1];
    SQLCHAR         sSqlState[SQL_SQLSTATE_SIZE + 1];
    SQLSMALLINT     sMsgLength;
 
    char             sData[4][64];
 
    memset(sParam, 0, sizeof(sParam));
 
    fscanf(aFp, "%s %s %hd %s %s %hd %lld %lld\n",
           sData[0], sData[1], &sParam[2].mShort,
           sData[2], sData[3], &sParam[5].mShort,
           &sParam[6].mLong, &sParam[7].mLong);
 
    sParam[0].mIP.mLength = SQL_APPEND_IP_STRING;
    sParam[0].mIP.mAddrString = sData[0];
 
    sParam[1].mIP.mLength = SQL_APPEND_IP_STRING;
    sParam[1].mIP.mAddrString = sData[1];
 
    sParam[3].mIP.mLength = SQL_APPEND_IP_STRING;
    sParam[3].mIP.mAddrString = sData[2];
 
    sParam[4].mIP.mLength = SQL_APPEND_IP_STRING;
    sParam[4].mIP.mAddrString = sData[3];
 
    sRC = SQLAppendDataV2(aStmt, sParam);
    if( !SQL_SUCCEEDED(sRC) )
    {
        if( SQLError(aEnv, aCon, aStmt, sSqlState, &sNativeError,
                     sErrorMsg, SQL_MAX_MESSAGE_LENGTH, &sMsgLength) != SQL_SUCCESS )
        {
            return RC_FAILURE;
        }
 
        printf("SQLSTATE-[%s], Machbase-[%d][%s]\n", sSqlState, sNativeError, sErrorMsg);
 
        if( sNativeError != 9604 &&
            sNativeError != 9605 &&
            sNativeError != 9606 )
        {
            return RC_FAILURE;
        }
        else
        {
            //data value error in one record, so return success to keep attending
        }
    }
    return RC_SUCCESS;
}
 
 
int appendF2(SQLHENV aEnv, SQLHDBC aCon, SQLHSTMT aStmt, FILE* aFp)
{
    SQL_APPEND_PARAM sParam[8];
    SQLRETURN        sRC;
 
    SQLINTEGER      sNativeError;
    SQLCHAR         sErrorMsg[SQL_MAX_MESSAGE_LENGTH + 1];
    SQLCHAR         sSqlState[SQL_SQLSTATE_SIZE + 1];
    SQLSMALLINT     sMsgLength;
 
    char             sData[4][64];
 
    memset(sParam, 0, sizeof(sParam));
 
    fscanf(aFp, "%s %s %hd %s %s %hd %lld %lld\n",
           sData[0], sData[1], &sParam[2].mShort,
           sData[2], sData[3], &sParam[5].mShort,
           &sParam[6].mLong, &sParam[7].mLong);
 
    sParam[0].mIP.mLength = SQL_APPEND_IP_STRING;
    sParam[0].mIP.mAddrString = sData[0];
 
    sParam[1].mIP.mLength = SQL_APPEND_IP_STRING;
    sParam[1].mIP.mAddrString = sData[1];
 
    sParam[3].mIP.mLength = SQL_APPEND_IP_STRING;
    sParam[3].mIP.mAddrString = sData[2];
 
    sParam[4].mIP.mLength = SQL_APPEND_IP_STRING;
    sParam[4].mIP.mAddrString = sData[3];
 
    sRC = SQLAppendDataV2(aStmt, sParam);
    if( !SQL_SUCCEEDED(sRC) )
    {
        if( SQLError(aEnv, aCon, aStmt, sSqlState, &sNativeError,
                     sErrorMsg, SQL_MAX_MESSAGE_LENGTH, &sMsgLength) != SQL_SUCCESS )
        {
            return RC_FAILURE;
        }
 
        printf("SQLSTATE-[%s], Machbase-[%d][%s]\n", sSqlState, sNativeError, sErrorMsg);
 
        if( sNativeError != 9604 &&
            sNativeError != 9605 &&
            sNativeError != 9606 )
        {
            return RC_FAILURE;
        }
        else
        {
            //data value error in one record, so return success to keep attending
        }
    }
    return RC_SUCCESS;
}
 
 
int appendEvent(SQLHENV aEnv, SQLHDBC aCon, SQLHSTMT aStmt, FILE* aFp)
{
    SQL_APPEND_PARAM sParam[3];
    SQLRETURN        sRC;
 
    SQLINTEGER      sNativeError;
    SQLCHAR         sErrorMsg[SQL_MAX_MESSAGE_LENGTH + 1];
    SQLCHAR         sSqlState[SQL_SQLSTATE_SIZE + 1];
    SQLSMALLINT     sMsgLength;
 
    char             sData[2][20];
 
    memset(sParam, 0, sizeof(sParam));
 
    fscanf(aFp, "%s %d %s\n",sData[0], &sParam[1].mInteger, sData[1]);
 
    sParam[0].mIP.mLength = SQL_APPEND_IP_STRING;
    sParam[0].mIP.mAddrString = sData[0];
 
    sParam[2].mVarchar.mLength = strlen(sData[1]);
    sParam[2].mVarchar.mData = sData[1];
 
    sRC = SQLAppendDataV2(aStmt, sParam);
    if( !SQL_SUCCEEDED(sRC) )
    {
        if( SQLError(aEnv, aCon, aStmt, sSqlState, &sNativeError,
                     sErrorMsg, SQL_MAX_MESSAGE_LENGTH, &sMsgLength) != SQL_SUCCESS )
        {
            return RC_FAILURE;
        }
 
        printf("SQLSTATE-[%s], Machbase-[%d][%s]\n", sSqlState, sNativeError, sErrorMsg);
 
        if( sNativeError != 9604 &&
            sNativeError != 9605 &&
            sNativeError != 9606 )
        {
            return RC_FAILURE;
        }
        else
        {
            //data value error in one record, so return success to keep attending
        }
    }
    return RC_SUCCESS;
}
 
 
void *eachThread(void *aIdx)
{
    SQLHENV    sEnv = SQL_NULL_HENV;
    SQLHDBC    sCon = SQL_NULL_HDBC;
    SQLHSTMT   sStmt[LOG_FILE_CNT] = {SQL_NULL_HSTMT,};
 
    FILE*      sFp;
    int        i;
    int        sLogType;
 
    int        sThrNo = *(int *)aIdx;
 
    // Alloc ENV and DBC
    if( connectDB(&sEnv, &sCon) == RC_SUCCESS )
    {
        printf("[%d]connectDB success.\n", sThrNo);
    }
    else
    {
        printf("[%d]connectDB failure.\n", sThrNo);
        goto error;
    }
 
    // set timed flush true
    if( SQLSetConnectAppendFlush(sCon, 1) != SQL_SUCCESS )
    {
        printError(sEnv, sCon, NULL, "SQLSetConnectAppendFlush Error");
        goto error;
    }
 
    for( i = 0; i < LOG_FILE_CNT; i++ )
    {
        // Alloc stmt
        if( SQLAllocStmt(sCon,&sStmt[i]) != SQL_SUCCESS )
        {
            printError(sEnv, sCon, sStmt[i], "SQLAllocStmt Error");
            goto error;
        }
 
        if( appendOpen(sEnv, sCon, sStmt[i], gTableName[i]) == RC_FAILURE )
        {
            printError(sEnv, sCon, sStmt[i], "SQLAppendOpen Error");
            goto error;
        }
        else
        {
            printf("[%d-%d]appendOpen success.\n", sThrNo, i);
        }
 
        if( SQLAppendSetErrorCallback(sStmt[i], appendDumpError) != SQL_SUCCESS )
        {
            printError(sEnv, sCon, sStmt[i], "SQLAppendSetErrorCallback Error");
            goto error;
        }
 
        // set timed flush interval as 2 seconds
        if( SQLSetStmtAppendInterval(sStmt[i], 2000) != SQL_SUCCESS )
        {
            printError(sEnv, sCon, sStmt[i], "SQLSetStmtAppendInterval Error");
            goto error;
        }
    }
 
    sFp = fopen((char*)gFileName[sThrNo], "rt");
    if( sFp == NULL )
    {
        printf("file open error - [%d][%s]\n", sThrNo, gFileName[sThrNo]);
    }
    else
    {
        printf("file open success - [%d][%s]\n", sThrNo, gFileName[sThrNo]);
 
        for( i = 0; !feof(sFp); i++ )
        {
            fscanf(sFp, "%d ", &sLogType);
            switch(sLogType)
            {
                case 1://f1
                    if( appendF1(sEnv, sCon, sStmt[0], sFp) == RC_FAILURE )
                    {
                        goto error;
                    }
                    break;
                case 2://f2
                    if( appendF2(sEnv, sCon, sStmt[1],sFp) == RC_FAILURE )
                    {
                        goto error;
                    }
                    break;
                case 3://event
                    if(appendEvent(sEnv, sCon, sStmt[2], sFp) == RC_FAILURE )
                    {
                        goto error;
                    }
                    break;
                default:
                    printf("unknown type error\n");
                    break;
            }
 
            if( (i%10000) == 0 )
            {
                fprintf(stdout, ".");
                fflush(stdout);
            }
        }
        printf("\n");
 
        fclose(sFp);
    }
 
    for( i = 0; i < LOG_FILE_CNT; i++)
    {
        printf("[%d-%d]appendClose start...\n", sThrNo, i);
        if( appendClose(sEnv, sCon, sStmt[i]) == RC_FAILURE )
        {
            printf("[%d-%d]appendClose failure\n", sThrNo, i);
        }
        else
        {
            printf("[%d-%d]appendClose success\n", sThrNo, i);
        }
 
        if( SQLFreeStmt(sStmt[i], SQL_DROP) != SQL_SUCCESS )
        {
            printError(sEnv, sCon, sStmt[i], "SQLFreeStmt Error");
        }
        sStmt[i] = SQL_NULL_HSTMT;
    }
 
    disconnectDB(sEnv, sCon);
 
    printf("[%d]disconnected.\n", sThrNo);
 
    pthread_exit(NULL);
 
error:
    for( i = 0; i < LOG_FILE_CNT; i++)
    {
        if( sStmt[i] != SQL_NULL_HSTMT )
        {
            appendClose(sEnv, sCon, sStmt[i]);
 
            if( SQLFreeStmt(sStmt[i], SQL_DROP) != SQL_SUCCESS )
            {
                printError(sEnv, sCon, sStmt[i], "SQLFreeStmt Error");
            }
            sStmt[i] = SQL_NULL_HSTMT;
        }
    }
 
    if( sCon != SQL_NULL_HDBC )
    {
        disconnectDB(sEnv, sCon);
    }
 
    pthread_exit(NULL);
}
 
 
int initTables()
{
    SQLHENV     sEnv  = SQL_NULL_HENV;
    SQLHDBC     sCon  = SQL_NULL_HDBC;
 
    if( connectDB(&sEnv, &sCon) == RC_SUCCESS )
    {
        printf("connectDB success.\n");
    }
    else
    {
        printf("connectDB failure.\n");
        goto error;
    }
 
    if( createTables(sEnv, sCon) == RC_SUCCESS )
    {
        printf("createTables success.\n");
    }
    else
    {
        printf("createTables failure.\n");
        goto error;
    }
 
    disconnectDB(sEnv, sCon);
 
    return RC_SUCCESS;
 
error:
 
    if( sCon != SQL_NULL_HDBC )
    {
        disconnectDB(sEnv, sCon);
    }
 
    return RC_FAILURE;
}
 
 
int main()
{
    pthread_t sThread[MAX_THREAD_NUM];
    int       sNum[MAX_THREAD_NUM];
    int       sRC;
    int       i;
 
    initTables();
 
    //
    //eachThread has own ENV,DBC and STMT
    //
    for(i = 0; i < MAX_THREAD_NUM; i++)
    {
        sNum[i] = i;
 
        sRC = pthread_create(&sThread[i], NULL, (void *)eachThread, (void*)&sNum[i]);
        if ( sRC != RC_SUCCESS )
        {
            printf("Error in Thread create[%d] : %d\n", i, sRC);
            return RC_FAILURE;
        }
    }
 
    for(i = 0; i < MAX_THREAD_NUM; i++)
    {
        sRC = pthread_join(sThread[i], NULL);
        if( sRC != RC_SUCCESS )
        {
            printf("Error in Thread[%d] : %d\n", i, sRC);
            return RC_FAILURE;
        }
        printf("%d thread join\n", i+1);
    }
 
    return RC_SUCCESS;
}
