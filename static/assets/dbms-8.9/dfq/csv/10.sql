SELECT id,label
FROM READ('/srv/dfq/nulls.csv',
 'format=csv',
 'header=true',
 'type.id=LONG',
 'type.v=LONG',
 'type.label=TEXT',
 'null_values=NULL',
 'allow_quoted_nulls=true',
 'null_padding=true',
 'force_not_null=id') ORDER BY id;
