import json,math,bisect
R=math.radians; D=math.degrees; C=299792.458; Re=6371.0088
A='/home/claude/mh370-model-atlas/data/'
sat=json.load(open(A+'satstate.json')); ev=json.load(open(A+'events_canon.json'))
S=[]
for r in sat:
    d=0 if r['t'][8:10]=='07' else 1
    h,m=int(r['t'][11:13]),int(r['t'][14:16])
    S.append((d*86400+h*3600+m*60,r['x'],r['y'],r['z'],r['lat'],r['lon']))
S.sort(); ts=[p[0] for p in S]
def satat(T):
    i=max(0,min(len(S)-2,bisect.bisect_left(ts,T)-1)); a,b=S[i],S[i+1]
    f=0 if b[0]==a[0] else (T-a[0])/(b[0]-a[0])
    return [a[j]+f*(b[j]-a[j]) for j in range(1,6)]
def secs(t):
    d=0 if t[8:10]=='07' else 1
    return d*86400+int(t[11:13])*3600+int(t[14:16])*60+int(t[17:19])
PLAT,PLON=-31.80,115.887
px=Re*math.cos(R(PLAT))*math.cos(R(PLON)); py=Re*math.cos(R(PLAT))*math.sin(R(PLON)); pz=Re*math.sin(R(PLAT))
h=40000*0.3048/1000.0
def geom(T):
    x,y,z,la,lo=satat(T)
    return math.sqrt(x*x+y*y+z*z), math.sqrt((x-px)**2+(y-py)**2+(z-pz)**2), la, lo
def slant(th,rsat): 
    ra=Re+h; return math.sqrt(rsat*rsat+ra*ra-2*rsat*ra*math.cos(R(th)))
def theta(d,rsat):
    lo_,hi=0.1,80.0
    for _ in range(200):
        mid=(lo_+hi)/2
        if slant(mid,rsat)<d: lo_=mid
        else: hi=mid
    return (lo_+hi)/2

rows=sorted([(r['timestamp_utc'],float(r['canonical_bto_us'])) for r in ev
             if r['included_for_bto']=='True' and r['canonical_bto_us']],key=lambda r:secs(r[0]))
# calibrate the bias on the PUBLISHED arc 7 alone
t7='2014-03-08T00:19:29Z'; bto7=[b for t,b in rows if t==t7][0]
rs7,rp7,_,_=geom(secs(t7))
bias=bto7-2*(slant(44.4701,rs7)+rp7)/C*1e6
print('bias calibrated on the published 7th arc alone: %.2f us'%bias)
print('  (station assumed at %.3f, %.3f -- SUPPLIED, not from the project archive)'%(PLAT,PLON))
print()
print('%-10s %8s %10s %10s %12s'%('time','BTO us','theta deg','sub lon','check'))
out=[]
for t,bto in rows:
    rs,rp,la,lo=geom(secs(t))
    d=(bto-bias)*1e-6*C/2-rp
    th=theta(d,rs)
    chk=''
    if t=='2014-03-07T19:41:03Z': chk='arc1 %+.2f km'%((th-29.4182)*111.19)
    if t==t7: chk='arc7 %+.2f km'%((th-44.4701)*111.19)
    out.append({'t':t,'bto':bto,'theta':round(th,4),'sublat':round(la,4),'sublon':round(lo,4)})
    print('%-10s %8.0f %10.4f %10.4f %12s'%(t[11:19],bto,th,lo,chk))
json.dump(out,open('rings_v2.json','w'),indent=1)
print()
a1=[o for o in out if o['t']=='2014-03-07T19:41:03Z'][0]['theta']
print('INDEPENDENT CHECK: project arc-1 ring radius 29.4182 deg')
print('  derived from canonical BTO + published ephemeris + station leg: %.4f deg'%a1)
print('  difference: %.4f deg = %.2f km'%(a1-29.4182,(a1-29.4182)*111.19))
print('  for scale, the published arc 7 itself scatters 4.11 km about its own circle')

# ---- does the derived ring, centred on the true subsatellite point, reproduce the published arc 7?
arc=json.load(open(A+'arc7.json'))
rs,rp,la7,lo7=geom(secs(t7))
def ang(la1,lo1,la2,lo2):
    return D(math.acos(min(1,max(-1,math.sin(R(la1))*math.sin(R(la2))+math.cos(R(la1))*math.cos(R(la2))*math.cos(R(lo2-lo1))))))
th7=[o for o in out if o['t']==t7][0]['theta']
res=[(ang(la7,lo7,p[1],p[0])-th7)*111.19 for p in arc['lonlat']]
print()
print('derived ring about the TRUE subsatellite point (%.4f N, %.4f E), theta %.4f deg'%(la7,lo7,th7))
print('  vs the 200 published arc points: mean %+.2f km, sd %.2f km, max |%.2f| km'%(
      sum(res)/len(res),(sum((r-sum(res)/len(res))**2 for r in res)/len(res))**.5,max(abs(r) for r in res)))
print("  project's stored ring centre: 0.5327 N, 64.3347 E   subsatellite point: %.4f N, %.4f E"%(la7,lo7))
print('  separation of the two centres: %.2f km'%(ang(0.5327,64.3347,la7,lo7)*111.19))
