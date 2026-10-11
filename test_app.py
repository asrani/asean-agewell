from pathlib import Path
from streamlit.testing.v1 import AppTest
app=Path(__file__).with_name('app.py')
at=AppTest.from_file(str(app), default_timeout=60).run()
assert not at.exception
assert at.metric[0].value=='12'
at.sidebar.radio[0].set_value('New screening').run()
assert not at.exception
at.text_input[0].set_value('DEMO-NEW')
at.checkbox[-1].check()
at.radio[0].set_value('Illustrative AI output') if at.radio[0].label=='Measurement source' else at.radio[1].set_value('Illustrative AI output')
next(b for b in at.button if b.label=='Save screening for review').click().run()
assert not at.exception
assert len(at.session_state['records'])==13
r=at.session_state['records'][-1]
assert r['walk_seconds']==6.4 and r['status']=='Awaiting review'
next(b for b in at.button if b.label=='Save screening for review').click().run()
assert len(at.session_state['records'])==13 and len(at.error)==1
at.text_input[0].set_value('DEMO-MISSING')
next(x for x in at.radio if x.label=='Measurement source').set_value('Not assessed')
next(b for b in at.button if b.label=='Save screening for review').click().run()
assert at.session_state['records'][-1]['walk_seconds'] is None
at.sidebar.radio[0].set_value('Referral tracker').run()
next(x for x in at.selectbox if x.label=='Choose a record to update').set_value('DEMO-NEW').run()
next(x for x in at.selectbox if x.label=='Referral status').set_value('Follow-up complete')
next(b for b in at.button if b.label=='Save follow-up').click().run()
assert not at.exception
assert next(r for r in at.session_state['records'] if r['id']=='DEMO-NEW')['status']=='Follow-up complete'
at.sidebar.radio[0].set_value('About the pilot').run()
assert not at.exception
print('PASS: pages, simulated screening, duplicate prevention, missing measurements, referral update')
