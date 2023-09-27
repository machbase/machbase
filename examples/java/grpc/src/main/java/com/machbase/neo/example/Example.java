package com.machbase.neo.example;

import java.time.LocalDateTime;
import java.time.ZoneOffset;
import java.time.format.DateTimeFormatter;
import java.util.ArrayList;
import java.util.List;

import com.google.protobuf.Any;
import com.google.protobuf.DoubleValue;
import com.machbase.neo.rpc.*;
import com.machbase.neo.rpc.MachbaseGrpc.MachbaseBlockingStub;
import com.machbase.neo.rpc.Machrpc.Column;
import com.machbase.neo.rpc.Machrpc.ColumnsResponse;
import com.machbase.neo.rpc.Machrpc.QueryRequest;
import com.machbase.neo.rpc.Machrpc.QueryResponse;
import com.machbase.neo.rpc.Machrpc.RowsFetchResponse;
import com.google.protobuf.Int32Value;
import com.google.protobuf.StringValue;
import com.google.protobuf.Timestamp;

import io.grpc.Grpc;
import io.grpc.InsecureChannelCredentials;
import io.grpc.ManagedChannel;;

public class Example {
    public static void main(String[] args) throws Exception {
        ManagedChannel channel = Grpc.newChannelBuilder("127.0.0.1:5655", InsecureChannelCredentials.create()).build();
        MachbaseBlockingStub stub = MachbaseGrpc.newBlockingStub(channel);

        QueryRequest.Builder builder = Machrpc.QueryRequest.newBuilder();
        builder.setSql("select * from example order by time desc limit ?");
        builder.addParams(Any.pack(Int32Value.of(10)));

        QueryRequest req = builder.build();
        QueryResponse rsp = stub.query(req);

        try {
            ColumnsResponse cols = stub.columns(rsp.getRowsHandle());
            ArrayList<String> headers = new ArrayList<String>();
            headers.add("RowNum");
            for (int i = 0; i < cols.getColumnsCount(); i++) {
                Column c = cols.getColumns(i);
                headers.add(c.getName() + "(" + c.getType() + ")");
            }

            int nrow = 0;
            RowsFetchResponse fetch = null;
            while (true) {
                fetch = stub.rowsFetch(rsp.getRowsHandle());
                if (fetch == null || fetch.getHasNoRows()) {
                    break;
                }
                nrow++;
            
                ArrayList<String> line = new ArrayList<String>();
                line.add(Integer.toString(nrow, 10));
                List<Any> row = fetch.getValuesList();
                for (Any anyv : row) {
                    line.add(convpb(anyv));
                }
                System.out.println(String.join("    ", line));
            }
        } finally {
            stub.rowsClose(rsp.getRowsHandle());
            channel.shutdown();
        }
    }

    static DateTimeFormatter sdf = DateTimeFormatter.ofPattern("yyyy.MM.dd HH:mm:ss.SSS");

    static String convpb(Any any) {
        try {
            switch (any.getTypeUrl()) {
                case "type.googleapis.com/google.protobuf.StringValue": {
                    StringValue v = any.unpack(StringValue.class);
                    return v.getValue();
                }
                case "type.googleapis.com/google.protobuf.Timestamp": {
                    Timestamp v = any.unpack(Timestamp.class);
                    LocalDateTime ldt = java.time.LocalDateTime.ofEpochSecond(v.getSeconds(), v.getNanos(), ZoneOffset.UTC);
                    return ldt.format(sdf);
                }
                case "type.googleapis.com/google.protobuf.DoubleValue": {
                    DoubleValue v = any.unpack(DoubleValue.class);
                    return Double.toString(v.getValue());
                }
                default:
                    return "unsupproted " + any.getTypeUrl();
            }
        } catch (Exception e) {
            return "error " + e.getMessage();
        }
    }
}