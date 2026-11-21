-- Each statement below must fail. Run it separately from array.sql.
CREATE LOG TABLE M89_ARRAY_BAD(ID INTEGER, A DOUBLE[65537]);
SELECT ARRAY_AT(ARRAY[1,2],2);
SELECT ARRAY_SLICE(ARRAY[1,2],0,1,0);
SELECT ID,ARRAY_LENGTH(PAYLOAD) FROM READ('/srv/dfq/array-read/payload.jsonl',
 'format=jsonl','project.id=id','type.id=LONG','project.payload=payload','type.payload=DOUBLE[2]');
SELECT ARRAY_LENGTH(PAYLOAD) FROM READ('/srv/dfq/array-read/bad-payload.jsonl',
 'format=jsonl','project.payload=payload','type.payload=DOUBLE[65536]');
