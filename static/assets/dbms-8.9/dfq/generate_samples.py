from pathlib import Path
import csv,json,gzip,shutil
import numpy as np
import pyarrow as pa
import pyarrow.parquet as pq
import h5py
from mcap.writer import Writer
p=Path(__import__('sys').argv[1]);p.mkdir(parents=True,exist_ok=True)
rows=[{'id':i,'v':i*10,'label':f'sensor-{i}','day':'2026-11-01','pose':{'x':i*0.5},'items':[i,i+1]} for i in range(1,6)]
for fmt,sep in [('csv',','),('tsv','\t')]:
 for name,header,delim in [(f'sensor.{fmt}',True,sep),(f'no-header.{fmt}',False,sep),(f'semicolon.{fmt}',True,';')]:
  with (p/name).open('w',newline='') as f:
   w=csv.writer(f,delimiter=delim)
   if header:w.writerow(['id','v','label','day'])
   w.writerows([[r['id'],r['v'],r['label'],r['day']] for r in rows])
 for n in (1,2):shutil.copyfile(p/f'sensor.{fmt}',p/f'part-{n}.{fmt}')
 with gzip.open(p/f'sensor.{fmt}.gz','wb') as f:f.write((p/f'sensor.{fmt}').read_bytes())
 (p/f'bad.{fmt}').write_text('id'+sep+'v\n1'+sep+'wrong\n')
(p/'sensor.json').write_text(json.dumps(rows));(p/'sensor.jsonl').write_text('\n'.join(json.dumps(r) for r in rows)+'\n')
(p/'wrapped.json').write_text(json.dumps({'items':rows}));(p/'wrapped.jsonl').write_text(json.dumps({'items':rows})+'\n')
for fmt in ('json','jsonl'):
 for n in (1,2):shutil.copyfile(p/f'sensor.{fmt}',p/f'part-{n}.{fmt}')
 with gzip.open(p/f'sensor.{fmt}.gz','wb') as f:f.write((p/f'sensor.{fmt}').read_bytes())
 (p/f'bad.{fmt}').write_text('{broken')
table=pa.Table.from_pylist(rows)
for name in ('sensor.parquet','part-1.parquet','part-2.parquet'):pq.write_table(table,p/name,compression='snappy')
arr=np.array([(r['id'],r['v']) for r in rows],dtype=[('id','<i8'),('v','<i8')]);np.save(p/'sensor.npy',arr)
np.save(p/'matrix.npy',np.arange(10,dtype='<i8').reshape(5,2));np.save(p/'tensor.npy',np.arange(20,dtype='<i8').reshape(5,2,2))
np.savez_compressed(p/'arrays.npz',main=arr,matrix=np.arange(10,dtype='<i8').reshape(5,2))
for fmt in ('npy','npz'):
 for n in (1,2):shutil.copyfile(p/('sensor.npy' if fmt=='npy' else 'arrays.npz'),p/f'part-{n}.{fmt}')
(p/'bad.npy').write_bytes(b'broken');(p/'bad.npz').write_bytes(b'broken');(p/'bad.parquet').write_bytes(b'broken')
with h5py.File(p/'sensor.h5','w') as f:
 f.create_dataset('records',data=arr)
 g=f.create_group('table');g.create_dataset('id',data=np.arange(1,6,dtype='<i8'));g.create_dataset('v',data=np.arange(1,6,dtype='<i8')*10)
 f.create_dataset('matrix',data=np.arange(10,dtype='<i8').reshape(5,2));f.attrs['unit']='sample'
(p/'bad.h5').write_bytes(b'broken')
with (p/'sensor.mcap').open('wb') as f:
 w=Writer(f);w.start();sid=w.register_schema(name='Sensor',encoding='jsonschema',data=json.dumps({'type':'object','properties':{'id':{'type':'integer'},'v':{'type':'integer'}}}).encode());ch=w.register_channel(topic='/sensor',message_encoding='json',schema_id=sid)
 for i,r in enumerate(rows):w.add_message(channel_id=ch,log_time=1000000000+i,publish_time=1000000000+i,data=json.dumps({'id':r['id'],'v':r['v']}).encode(),sequence=i)
 w.finish()
(p/'bad.mcap').write_bytes(b'broken')
(p/'README.txt').write_text('Generated synthetic sensor samples: id=1..5; v=id*10; COUNT=5, SUM(id)=15, SUM(v)=150.\n')

for fmt,sep in [('csv',';'),('tsv','\t')]:
 (p/f'locale.{fmt}').write_text(f'id{sep}v\n1{sep}1.234,50\n2{sep}2.000,25\n')
 sep=',' if fmt=='csv' else '\t'
 (p/f'nulls.{fmt}').write_text(f'id{sep}v{sep}label\n1{sep}10{sep}NULL\n2{sep}20{sep}"NULL"\n3{sep}30\n')
 (p/f'comments.{fmt}').write_text(f'banner\n# comment\n1{sep}10{sep}a\n2{sep}20{sep}b\n')
