import json,sys
d=json.load(open(sys.argv[1] if len(sys.argv)>1 else "data/raw/hhs_capacity_ccn220071.json"))
def f(r,k):
    v=r.get(k)
    try:
        v=float(v); return None if v<0 else v
    except: return None
rows=[]
for r in d:
    w=r['collection_week'][:10]
    tb=f(r,'total_beds_7_day_avg'); ib=f(r,'inpatient_beds_7_day_avg'); iu=f(r,'inpatient_beds_used_7_day_avg')
    ab=f(r,'all_adult_hospital_inpatient_beds_7_day_avg'); ao=f(r,'all_adult_hospital_inpatient_bed_occupied_7_day_avg')
    icb=f(r,'total_staffed_adult_icu_beds_7_day_avg'); ico=f(r,'staffed_adult_icu_bed_occupancy_7_day_avg')
    tib=f(r,'total_icu_beds_7_day_avg'); tiu=f(r,'icu_beds_used_7_day_avg')
    cov=f(r,'inpatient_beds_used_covid_7_day_avg'); covicu=f(r,'staffed_icu_adult_patients_confirmed_and_suspected_covid_7_day_avg')
    ed=f(r,'previous_day_total_ed_visits_7_day_sum'); edc=f(r,'previous_day_covid_ed_visits_7_day_sum')
    adm=f(r,'previous_day_admission_adult_covid_confirmed_7_day_sum')
    rows.append(dict(w=w,tb=tb,ib=ib,iu=iu,ab=ab,ao=ao,icb=icb,ico=ico,tib=tib,tiu=tiu,cov=cov,covicu=covicu,ed=ed,edc=edc,adm=adm))
miss={k:sum(1 for r in rows if r[k] is None) for k in rows[0]}
print(miss)
for r in rows[::20]: print(r)
json.dump([{k:(round(v,1) if isinstance(v,float) else v) for k,v in r.items()} for r in rows],open("data/weeks.json","w"),separators=(',',':'))
