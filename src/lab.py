"""Synthetic, authorized API telemetry experiment. No network activity."""
import argparse,csv,json,random,statistics
from pathlib import Path

FIELDS=['scenario','session','split','requests','duration_s','rps','error_rate','unique_paths','path_entropy','mean_interval','interval_cv','sensitive_attempts','label_malicious','automation_type']
PATHS=['/health','/products','/profile','/orders','/help','/search','/admin','/internal/export']

def entropy(values):
    from math import log2
    counts={x:values.count(x) for x in set(values)}
    n=len(values)
    return -sum((v/n)*log2(v/n) for v in counts.values())

def generate(seed=42, per_group=180):
    rng=random.Random(seed)
    rows=[]
    for group in ['legitimate','scripted_probe','adaptive_probe']:
        for i in range(per_group):
            # Deliberately overlapping behaviors: origin cannot be inferred perfectly.
            if group=='legitimate':
                n=rng.randint(8,65); duration=rng.uniform(45,360); error=rng.uniform(0,.12); sensitive=0
                paths=rng.choices(PATHS[:6],k=n)
            elif group=='scripted_probe':
                n=rng.randint(55,180); duration=rng.uniform(15,100); error=rng.uniform(.12,.62); sensitive=rng.randint(1,12)
                paths=rng.choices(PATHS,k=n)
            else:
                n=rng.randint(25,110); duration=rng.uniform(25,220); error=rng.uniform(.05,.42); sensitive=rng.randint(0,8)
                paths=rng.choices(PATHS,k=n)
            mean_interval=duration/max(1,n-1)
            cv=max(.03,rng.gauss(.28 if group=='scripted_probe' else .9,.18))
            rows.append(dict(scenario=group,session=f'{group}-{i:04}',split='test' if i%5==0 else 'train',requests=n,duration_s=round(duration,3),rps=round(n/duration,5),error_rate=round(error,4),unique_paths=len(set(paths)),path_entropy=round(entropy(paths),4),mean_interval=round(mean_interval,4),interval_cv=round(cv,4),sensitive_attempts=sensitive,label_malicious=int(group!='legitimate'),automation_type='none' if group=='legitimate' else ('script' if group=='scripted_probe' else 'simulated_adaptive')))
    rng.shuffle(rows)
    return rows

def rule_predict(row):
    return int(float(row['rps'])>1.15 or float(row['error_rate'])>.3 or int(row['sensitive_attempts'])>=3)

def metrics(rows, predictions):
    y=[int(r['label_malicious']) for r in rows]
    tp=sum(a==1 and b==1 for a,b in zip(y,predictions));tn=sum(a==0 and b==0 for a,b in zip(y,predictions))
    fp=sum(a==0 and b==1 for a,b in zip(y,predictions));fn=sum(a==1 and b==0 for a,b in zip(y,predictions))
    safe=lambda a,b:round(a/b,4) if b else 0.0
    precision=safe(tp,tp+fp);recall=safe(tp,tp+fn)
    return dict(tp=tp,tn=tn,fp=fp,fn=fn,precision=precision,recall=recall,f1=safe(2*precision*recall,precision+recall),false_positive_rate=safe(fp,fp+tn))

def main():
    p=argparse.ArgumentParser();p.add_argument('--seed',type=int,default=42);p.add_argument('--per-group',type=int,default=180);p.add_argument('--output',default='data/synthetic_sessions.csv');p.add_argument('--results',default='results/baseline.json');args=p.parse_args()
    rows=generate(args.seed,args.per_group)
    out=Path(args.output);out.parent.mkdir(parents=True,exist_ok=True)
    with out.open('w',newline='',encoding='utf8') as f:
        w=csv.DictWriter(f,fieldnames=FIELDS);w.writeheader();w.writerows(rows)
    test=[r for r in rows if r['split']=='test']
    result={'experiment':'A0 synthetic rule baseline','seed':args.seed,'train_sessions':sum(r['split']=='train' for r in rows),'test_sessions':len(test),'test_metrics':metrics(test,[rule_predict(r) for r in test]),'limitations':'Synthetic, hand-designed distributions; not evidence of detection of real AI-driven attacks or AI attribution.'}
    dest=Path(args.results);dest.parent.mkdir(parents=True,exist_ok=True);dest.write_text(json.dumps(result,indent=2),encoding='utf8')
    print(json.dumps(result,indent=2))
if __name__=='__main__':main()
