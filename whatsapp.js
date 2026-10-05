/* Explicit desktop route and a recoverable order message; never auto-send. */
(() => {
  'use strict';
  function enhance(root) {
    const links=[...(root.matches?.('a[data-product-id]')?[root]:[]),...root.querySelectorAll('a[data-product-id]')];
    for(const link of links){
      if(!link.dataset.productId||link.dataset.webEnhanced)continue;
      const original=new URL(link.href,location.href);
      if(original.hostname!=='wa.me'||original.pathname!=='/923430173923')continue;
      link.dataset.webEnhanced='true';
      const message=original.searchParams.get('text')||'';
      const web=new URL('https://web.whatsapp.com/send/');
      web.searchParams.set('phone','923430173923');web.searchParams.set('text',message);
      const options=document.createElement('span');options.className='order-alternatives';
      const browser=document.createElement('a');browser.href=web.href;browser.target='_blank';browser.rel='noopener noreferrer';browser.className='whatsapp-web-link';browser.textContent='WhatsApp Web';browser.dataset.waProduct=link.dataset.productId;
      browser.title='Open in your computer browser. Link your WhatsApp account first if asked.';
      const copy=document.createElement('button');copy.type='button';copy.textContent='Copy order details';
      const status=document.createElement('span');status.className='order-copy-status';status.setAttribute('role','status');
      copy.addEventListener('click',async()=>{
        try {await navigator.clipboard.writeText(message);status.textContent='Copied. Paste into your WhatsApp chat.';}
        catch {
          status.textContent='Select and copy these details:';
          let field=options.querySelector('textarea');
          if(!field){field=document.createElement('textarea');field.readOnly=true;field.setAttribute('aria-label','Order details to copy');options.append(field);}
          field.value=message;field.focus();field.select();
        }
      });
      options.append(browser,copy,status);link.insertAdjacentElement('afterend',options);
    }
  }
  enhance(document);
  new MutationObserver(records=>{
    for(const record of records)for(const node of record.addedNodes)if(node.nodeType===1)enhance(node);
  }).observe(document.body,{childList:true,subtree:true});
})();
