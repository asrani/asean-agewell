from datetime import date, timedelta
import json
import pandas as pd
import streamlit as st

st.set_page_config(page_title='ASEAN AgeWell', page_icon='🌿', layout='wide')
st.markdown('''<style>
.block-container{padding-top:2rem;max-width:1200px}
[data-testid="stMetric"]{background:#edf5f1;border:1px solid #d9e6df;border-radius:14px;padding:18px}
h1,h2,h3{letter-spacing:-.035em}
[data-testid="stSidebar"]{background:#edf5f1}
</style>''', unsafe_allow_html=True)

COUNTRIES = ['Malaysia', 'Indonesia']
STATUS = ['Awaiting review', 'Referral arranged', 'Follow-up complete']

def seed():
    rows = []
    for i in range(12):
        rows.append(dict(id=f'DEMO-{i+1:03}', country=COUNTRIES[i % len(COUNTRIES)], age=62+i*2,
            date=str(date.today()-timedelta(days=i*2)), mobility_difficulty=i%3==0,
            falls=i%3, walking_aid=i%4==0, measurement='Illustrative sample',
            walk_seconds=round(4.2+i*.35,2), distance=4.0, chair_seconds=round(10+i*.8,1),
            status=STATUS[i%3], due=str(date.today()+timedelta(days=i-4)), notes='Synthetic demonstration record.'))
    return rows

if 'records' not in st.session_state:
    st.session_state.records = seed()

with st.sidebar:
    st.title('🌿 AgeWell')
    st.caption('MALAYSIA · INDONESIA')
    page = st.radio('Workspace', ['Overview', 'New screening', 'Referral tracker', 'About the pilot'])
    st.divider()
    st.caption('DEMONSTRATION WORKSPACE')
    st.write('Synthetic participants · Human-reviewed care')
    st.caption('Records live only in this browser session. Download before closing; no cloud sync or database is connected.')
    if st.button('Reset demo records'):
        st.session_state.records = seed()
        st.session_state.pop('latest', None)
        st.rerun()

st.caption('ASEAN AGEWELL / COMMUNITY MOBILITY')
st.title({'Overview':'A clearer view of community care.', 'New screening':'Make every community visit count.', 'Referral tracker':'Keep follow-up moving.', 'About the pilot':'Built for a regional research pilot.'}[page])
st.info('Prototype only. Use fictional data. No validated AI model, diagnosis, fall-risk score, or treatment recommendation is provided.')
# Keep older session records intact, but show only the current pilot countries.
records = [r for r in st.session_state.records if r['country'] in COUNTRIES]
df = pd.DataFrame(records, columns=list(seed()[0]))

if page == 'Overview':
    st.write('Explore community screening activity and the next steps recorded by health workers.')
    cols = st.columns(4)
    cols[0].metric('Screenings', len(records))
    cols[1].metric('Awaiting review', sum(r['status']==STATUS[0] for r in records))
    cols[2].metric('Referrals arranged', sum(r['status']==STATUS[1] for r in records))
    cols[3].metric('Follow-ups complete', sum(r['status']==STATUS[2] for r in records))
    left,right=st.columns([3,2])
    with left:
        st.subheader('Community reach')
        st.bar_chart(df.groupby('country').size().rename('Screenings'), color='#187565')
    with right:
        st.subheader('Your demonstration journey')
        st.markdown('**01 · Screen**\n\nRecord a fictional participant and mobility observations.\n\n**02 · Review**\n\nInspect measurements and self-reported concerns.\n\n**03 · Follow through**\n\nRecord a referral status and next contact date.')
    st.subheader('Follow-up queue')
    pending=df[df.status!=STATUS[2]].sort_values('due')
    st.dataframe(pending[['id','country','status','due']], hide_index=True, width='stretch')
    st.caption('Dates are administrative reminders, not clinical urgency categories.')

elif page == 'New screening':
    st.write('A short, worker-assisted record. All saved screenings start in the human-review queue.')
    with st.form('screening', clear_on_submit=False):
        a,b,c=st.columns(3)
        participant=a.text_input('Fictional participant ID', placeholder='e.g. DEMO-101', max_chars=40)
        country=b.selectbox('Country', COUNTRIES)
        age=c.number_input('Age',60,110,70)
        st.subheader('1. Community observations')
        a,b,c=st.columns(3)
        difficulty=a.checkbox('Reported mobility difficulty')
        falls=b.number_input('Reported falls in past 12 months',0,50,0)
        aid=c.checkbox('Uses a walking aid')
        st.subheader('2. Mobility measurement')
        mode=st.radio('Measurement source', ['Not assessed', 'Manual observations', 'Illustrative AI output'], horizontal=True)
        st.caption('Illustrative AI output uses fixed sample values, not video analysis. Manual values below apply only to Manual observations. Do not perform an assessment solely for this demo.')
        a,b,c=st.columns(3)
        distance=a.number_input('Walk distance (metres)',1.0,20.0,4.0,.5)
        seconds=b.number_input('Walk time (seconds)',0.1,300.0,6.0,.1)
        chair=c.number_input('Five chair rises: time (seconds)',0.1,300.0,16.0,.1)
        notes=st.text_area('Worker notes (fictional only)', max_chars=1000)
        acknowledged=st.checkbox('I am using fictional data and understand that the AI output is simulated.')
        submitted=st.form_submit_button('Save screening for review', type='primary')
    if submitted:
        ident=participant.strip()
        if not acknowledged:
            st.error('Confirm fictional-data use before saving.')
        elif not ident:
            st.error('Enter a fictional participant ID.')
        elif any(r['id'].casefold()==ident.casefold() for r in records):
            st.error('This participant ID already exists. Use a unique ID for this demo.')
        else:
            missing=mode=='Not assessed'
            row=dict(id=ident,country=country,age=age,date=str(date.today()),mobility_difficulty=difficulty,
                falls=falls,walking_aid=aid,measurement=mode, distance=None if missing else (4.0 if mode=='Illustrative AI output' else distance),
                walk_seconds=None if missing else (6.4 if mode=='Illustrative AI output' else seconds),
                chair_seconds=None if missing else (17.2 if mode=='Illustrative AI output' else chair),
                status=STATUS[0],due=str(date.today()+timedelta(days=7)),notes=notes)
            st.session_state.records.append(row)
            st.session_state.latest=row.copy()
            st.success(f'Saved {ident} to the review queue.')
    if 'latest' in st.session_state and st.session_state.latest['country'] in COUNTRIES:
        r=st.session_state.latest
        st.subheader('Latest saved screening · '+r['id'])
        st.caption('Source: '+r['measurement'])
        a,b,c=st.columns(3)
        a.metric('Walking speed', 'Not assessed' if r['walk_seconds'] is None else f"{r['distance']/r['walk_seconds']:.2f} m/s")
        b.metric('Five chair rises', 'Not assessed' if r['chair_seconds'] is None else f"{r['chair_seconds']:.1f} s")
        c.metric('Next step', 'Worker review')
        observations=[]
        if r['mobility_difficulty']: observations.append('Participant reported mobility difficulty.')
        if r['falls']: observations.append(f"Participant reported {r['falls']} fall(s) in the past 12 months.")
        if r['walking_aid']: observations.append('Walking aid use recorded.')
        st.write(' '.join(observations) or 'No questionnaire concerns recorded. This does not establish normal mobility or absence of risk.')
        st.caption('Review with an appropriately qualified professional. Measurements are not interpreted against clinical thresholds in this prototype.')
        st.download_button('Download screening summary',json.dumps(r,indent=2),file_name='agewell_screening.json',mime='application/json')

elif page == 'Referral tracker':
    st.write('Track the actions agreed by a health worker. This demo does not send referrals or contact participants.')
    a,b=st.columns(2)
    country=a.selectbox('Filter country',['All countries']+COUNTRIES)
    status=b.selectbox('Filter status',['All statuses']+STATUS)
    filtered=[r for r in records if (country=='All countries' or r['country']==country) and (status=='All statuses' or r['status']==status)]
    if not filtered:
        st.info('No records match these filters.')
    else:
        view=pd.DataFrame(filtered)
        st.dataframe(view[['id','country','age','status','due','measurement']],hide_index=True,width='stretch')
        ident=st.selectbox('Choose a record to update',[r['id'] for r in filtered])
        r=next(r for r in records if r['id']==ident)
        with st.form('update_'+ident):
            a,b=st.columns(2)
            new_status=a.selectbox('Referral status',STATUS,index=STATUS.index(r['status']))
            due=b.date_input('Next contact date',date.fromisoformat(r['due']))
            note=st.text_area('Follow-up notes',r['notes'],max_chars=1000)
            if st.form_submit_button('Save follow-up',type='primary'):
                r.update(status=new_status,due=str(due),notes=note)
                st.rerun()
        st.download_button('Export filtered records (CSV)',view.to_csv(index=False),file_name='agewell_demo_records.csv',mime='text/csv')
    st.caption('Exports include fictional observations and notes. Downloaded files are outside session storage.')

else:
    st.subheader('A focused question')
    st.write('Pilot countries: Malaysia and Indonesia.')
    st.write('Can smartphone-assisted mobility measurements support reliable community screening across different ASEAN settings?')
    a,b=st.columns(2)
    with a:
        st.markdown('### Working in this prototype\n- Community screening and unique participant IDs\n- Manual measurement calculations\n- Clearly labelled, fixed illustrative AI measurements\n- Review queue and editable referral status\n- JSON summaries and CSV exports')
    with b:
        st.markdown('### Research and deployment still required\n- Real pose estimation and independent clinical validation\n- Locally adapted language interfaces and consent workflows\n- Authentication, encrypted durable storage, and access controls\n- Device-based offline capture and secure synchronisation\n- Approved assessment and referral protocols')
    st.subheader('Proposed 24-month pilot')
    st.table(pd.DataFrame({'Months':['1–6','7–15','16–21','22–24'],'Work':['Co-design, ethics and site agreements','Data collection and model development','Independent prospective validation','Evaluation and handover']}))
    st.write('Streamlit runs on a Python server. This local demo can work without internet after installation while that server is running; it is not a mobile offline application.')
    st.link_button('WHO ICOPE reference','https://www.who.int/publications/i/item/9789240103726')
    st.caption('The proposed workflow is inspired by community healthy-ageing research. It is not an official WHO assessment tool or a clinically validated implementation.')

st.divider()
st.caption('ASEAN AgeWell · Research prototype · Fictional data only')
