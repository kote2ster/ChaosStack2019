import json
import os
import sys




sAll = os.environ['GOOGLE_CREDENTIALS']

sEnd = '-----END PRIVATE KEY-----'
i1 = sAll.index('-----BEGIN PRIVATE KEY-----')
i2 = sAll.index(sEnd)+len(sEnd)

sJson = sAll[:i1]+sAll[i2:]
sJson = sJson.replace('\n','')
d = json.loads(sJson)

sPrivateKey = sAll[i1:i2]

d['private_key'] = sPrivateKey.replace('\n',' ').replace('\\n','\n')


sOut1 = json.dumps(d,indent=2)

with open(sys.argv[-1],'w') as fout:
    fout.write(sOut1)

