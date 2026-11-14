"""그래프 설정 SQL로준비한실습DB에서동일prepared 재귀문을재실행한다."""
import os
from machbaseAPI import connect

SQL='''WITH RECURSIVE R(NODE_ID,DEPTH) AS (
 SELECT node_id,CAST(0 AS LONG) FROM M89_G_NODE
 WHERE kb_id=:kb AND node_id=:seed
 UNION ALL
 SELECT E.target_id,R.depth+1 FROM M89_G_EDGE E,R
 WHERE E.kb_id=:kb AND E.state='APPROVED'
   AND E.source_id=R.node_id AND R.depth<:max_depth
)
SELECT NODE_ID,DEPTH FROM R ORDER BY DEPTH,NODE_ID'''


def main():
    conn=connect(host=os.environ['M89_HOST'],port=int(os.environ['M89_PORT']),
                 user=os.environ['M89_USER'],password=os.environ['M89_PASSWORD'])
    cur=conn.cursor(prepared=True)
    try:
        for seed,depth in [(2,2),(999,2),(2,1)]:
            cur.execute(SQL,dict(kb=1,seed=seed,max_depth=depth))
            rows=cur.fetchall()
            print('seed=',seed,'depth=',depth,'rows=',rows)
            expected=5 if seed==2 and depth==2 else 4 if seed==2 else 0
            if len(rows)!=expected:raise AssertionError('unexpected recursive row count')
    finally:
        cur.close()
        conn.close()


if __name__=='__main__':main()
