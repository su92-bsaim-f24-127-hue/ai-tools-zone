/* Bounded integration hooks forward to the existing Google tag when available.
   Cloudflare Web Analytics records visits separately. Never emit query/message text. */
(() => {
  'use strict';
  const sections=new Set(['home','products','categories','compare','alternatives','use-cases','guides','pricing','about','privacy','terms','faq']);
  const events=new Set(['page_view','product_view','product_page_view','category_view','comparison_view','alternative_view','guide_view','pricing_view','tool_search','filter_use','compare_add','tool_finder_start','tool_finder_complete','whatsapp_click','product_whatsapp_click','outbound_vendor_click','generate_lead','cta_click']);
  const validProductId=value=>typeof value==='string'&&/^[a-z0-9]+(?:-[a-z0-9]+)*$/.test(value);
  const canonical=document.querySelector('link[rel="canonical"]');
  const path=canonical ? new URL(canonical.href).pathname : '/404.html';
  const section=path.split('/').filter(Boolean)[0]||'home';
  const emit=(name,extra={})=>{
    if(!events.has(name))return;
    const detail={name,page:path,section:sections.has(section)?section:'other'};
    if(validProductId(extra.product))detail.product=extra.product;
    if(extra.value!==undefined)detail.value=extra.value;
    if(extra.currency)detail.currency=extra.currency;
    if(extra.label)detail.label=extra.label;
    document.dispatchEvent(new CustomEvent('aitz:measure',{detail}));
    if(typeof window.gtag==='function')window.gtag('event',name,detail);
    else if(Array.isArray(window.dataLayer))window.dataLayer.push({event:name,...detail});
  };
  window.aitzMeasure=emit;
  emit('page_view');
  const pageEvents={products:'product_view',categories:'category_view',compare:'comparison_view',alternatives:'alternative_view',guides:'guide_view',pricing:'pricing_view'};
  if(pageEvents[section]&&(path.split('/').filter(Boolean).length>1||section==='pricing')){
    const pid=document.querySelector('.buy-now[data-product-id]')?.dataset.productId;
    emit(pageEvents[section],{product:pid});
    if(section==='products')emit('product_page_view',{product:pid});
  }
  let lastClickTime=0;
  let lastClickTarget=null;
  document.addEventListener('click',event=>{
    const link=event.target.closest('a[href]');
    if(link){
      const now=Date.now();
      if(link===lastClickTarget && (now-lastClickTime)<800)return;
      lastClickTime=now;
      lastClickTarget=link;
      const url=new URL(link.href,location.href);
      if((url.hostname==='wa.me'&&/^\/\d{8,15}$/.test(url.pathname))||(url.hostname==='web.whatsapp.com'&&url.pathname==='/send/'&&/^\d{8,15}$/.test(url.searchParams.get('phone')||''))){
        const product=link.dataset.productId||link.dataset.waProduct;
        emit('whatsapp_click',{product});
        if(validProductId(product)){
          emit('product_whatsapp_click',{product});
          const price=link.dataset.price?Number(link.dataset.price):undefined;
          emit('generate_lead',{product,value:price,currency:'PKR'});
        }
      } else if(link.matches('main a[target="_blank"]')&&url.protocol==='https:'&&url.origin!==location.origin){
        emit('outbound_vendor_click');
      }
      if(link.matches('.button, .guide-cta, .inline-link, .details-button')){
        emit('cta_click',{label:(link.textContent||'').trim().slice(0,50)});
      }
    }
    if(event.target.closest('[data-finder]'))emit('tool_finder_start');
    if(event.target.closest('[data-category]'))emit('filter_use');
  });
  let searchTimer,budgetTimer;
  document.addEventListener('input',event=>{
    if(event.target.id==='search'){clearTimeout(searchTimer);searchTimer=setTimeout(()=>emit('tool_search'),500);}
    if(event.target.id==='budget-filter'){clearTimeout(budgetTimer);budgetTimer=setTimeout(()=>emit('filter_use'),500);}
  });
  document.addEventListener('change',event=>{
    if(['access-filter','intent-filter','duration-filter','sort'].includes(event.target.id))emit('filter_use');
  });
})();
