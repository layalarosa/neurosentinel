"""Optional ML baseline: pip install -r requirements.txt"""
import csv,json
from pathlib import Path
from sklearn.ensemble import RandomForestClassifier,IsolationForest
from sklearn.metrics import precision_recall_fscore_support, confusion_matrix,average_precision_score
FEATURES=['requests','duration_s','rps','error_rate','unique_paths','path_entropy','mean_interval','interval_cv','sensitive_attempts']
rows=list(csv.DictReader(open('data/synthetic_sessions.csv',encoding='utf8')))
train=[r for r in rows if r['split']=='train'];test=[r for r in rows if r['split']=='test']
X=lambda rs:[[float(r[k]) for k in FEATURES] for r in rs]
y=lambda rs:[int(r['label_malicious']) for r in rs]
clf=RandomForestClassifier(n_estimators=150,random_state=42,class_weight='balanced').fit(X(train),y(train))
pred=clf.predict(X(test));score=clf.predict_proba(X(test))[:,1]
p,r,f,_=precision_recall_fscore_support(y(test),pred,average='binary',zero_division=0)
res={'experiment':'A1 random forest synthetic baseline','precision':float(p),'recall':float(r),'f1':float(f),'pr_auc':float(average_precision_score(y(test),score)),'confusion_matrix':confusion_matrix(y(test),pred).tolist(),'warning':'Synthetic data only. Split by sessions, but distribution design can leak scenario cues; external validation required.'}
Path('results/ml_baseline.json').write_text(json.dumps(res,indent=2));print(json.dumps(res,indent=2))
