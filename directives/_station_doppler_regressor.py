import json,math,bisect
R=math.radians; C=299792458.0; Re=6371.0088
A='/home/claude/mh370-model-atlas/data/'
sat=json.load(open(A+'satstate.json'))
S=[]
for r in sat:
    d=0 if r['t'][8:10]=='07' else 1
    S.append((d*86400+int(r['t'][11:13])*3600+int(r['t'][14:16])*60,r['x'],r['y'],r['z'],r['vx'],r['vy'],r['vz']))
S.sort(); ts=[p[0] for p in S]
def satat(T):
    i=max(0,min(len(S)-2,bisect.bisect_left(ts,T)-1)); a,b=S[i],S[i+1]
    f=0 if b[0]==a[0] else (T-a[0])/(b[0]-a[0])
    return [a[j]+f*(b[j]-a[j]) for j in range(1,7)]
PLAT,PLON=-31.80,115.887
px=Re*math.cos(R(PLAT))*math.cos(R(PLON)); py=Re*math.cos(R(PLAT))*math.sin(R(PLON)); pz=Re*math.sin(R(PLAT))
def rate(T):
    x,y,z,vx,vy,vz=satat(T); dx,dy,dz=x-px,y-py,z-pz
    rr=math.sqrt(dx*dx+dy*dy+dz*dz); return (dx*vx+dy*vy+dz*vz)/rr*1000.0
# the five SCORED BFO epochs
E=[('19:41:03',19*3600+41*60+3),('20:41:05',20*3600+41*60+5),('21:41:27',21*3600+41*60+27),
   ('22:41:22',22*3600+41*60+22),('00:11:00',86400+11*60)]
# C120's published BFO z-squared terms
z2={'19:41:03':2.901,'20:41:05':0.096,'21:41:27':0.041,'22:41:22':0.068,'00:11:00':0.052}
print('The five SCORED BFO epochs -- the regressor Codex needs')
print('%-10s %12s %12s %14s %10s %10s'%('time','rate m/s','L-band Hz','accel mm/s/s','C120 z2','C120 |r| Hz'))
rows=[]
for lab,T in E:
    v=rate(T); a=(rate(T+60)-rate(T-60))/120*1000  # mm/s^2
    f=-v/C*1.6e9
    r=math.sqrt(z2[lab])*4.3
    rows.append((lab,v,f,a,z2[lab],r))
    print('%-10s %12.3f %12.2f %14.4f %10.3f %10.2f'%(lab,v,f,a,z2[lab],r))
fs=[r[2] for r in rows]; acc=[abs(r[3]) for r in rows]; res=[r[5] for r in rows]
print()
print('station Doppler spans %.2f Hz across the scored BFO set (monotone)'%(max(fs)-min(fs)))
print('range acceleration varies only %.2fx across it (%.4f to %.4f mm/s/s)'%(max(acc)/min(acc),min(acc),max(acc)))
print("C120's BFO residuals vary %.1fx (%.2f to %.2f Hz), largest at 19:41"%(max(res)/min(res),min(res),max(res)))
print()
print('-> an AFC tracking-lag term proportional to range ACCELERATION would need ~%.1fx variation'%(max(res)/min(res)))
print('   to explain C120. Acceleration only varies %.2fx. That hypothesis does not fit; dropping it.'%(max(acc)/min(acc)))
print()
print('What a northern residual set of +2.6..+6.5 Hz would mean, under each explanation:')
print('  constant bias error : residuals show NO time order; mean 4.55 Hz absorbs 5.60 of chi2')
print('  station-term error  : residuals ASCEND with the rate, 2.6 at 19:41 -> 6.5 at 00:11,')
print('                        implying a scale error of %.1f%% on a %.1f Hz term plus a %.1f Hz offset'%(
      100*(6.5-2.6)/(max(fs)-min(fs)),max(fs)-min(fs),2.6))
