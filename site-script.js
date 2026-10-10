document.documentElement.classList.add('js');
const params=new URLSearchParams(location.search);
function choose(kind,focus=false){
 document.querySelectorAll('.form-panel').forEach(p=>p.hidden=p.id!==kind);
 document.querySelectorAll('[data-form]').forEach(b=>b.setAttribute('aria-pressed',String(b.dataset.form===kind)));
 if(focus){const heading=document.querySelector('#'+kind+' h2');heading.tabIndex=-1;heading.focus({preventScroll:true});}
}
function sync(){if(document.querySelector('.form-panel'))choose(new URLSearchParams(location.search).get('type')==='business'?'business':'acquisition');}
sync();window.addEventListener('popstate',sync);
document.querySelectorAll('[data-form]').forEach(b=>b.addEventListener('click',()=>{history.pushState(null,'','?type='+b.dataset.form);choose(b.dataset.form,true);}));
document.querySelectorAll('form').forEach(f=>f.addEventListener('submit',async e=>{
 e.preventDefault();const status=f.querySelector('[role=status]');status.classList.remove('hidden');
 if(document.documentElement.dataset.delivery==='preview'||location.hostname==='localhost'||location.hostname==='127.0.0.1'||location.protocol==='file:'){
  status.textContent='This review does not send or store information. Both inquiry paths will be activated and tested on Netlify before launch.';return;
 }
 const button=f.querySelector('button[type=submit]');button.disabled=true;status.textContent='Sending your inquiry…';
 try{
  const body=new URLSearchParams(new FormData(f));
  const response=await fetch('/',{method:'POST',headers:{'Content-Type':'application/x-www-form-urlencoded'},body:body.toString()});
  if(!response.ok)throw new Error('Submission failed');
  location.assign('/thank-you/');
 }catch(error){status.textContent='Your inquiry could not be sent. Your entries are still here. Please try again, or email robertritch@ritchventures.com.';button.disabled=false;}
}));
