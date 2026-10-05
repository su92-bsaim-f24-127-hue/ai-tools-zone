/* Local, bounded integration hooks. Cloudflare Web Analytics records page visits,
   not these events. No event collector is configured. Never emit query/message text. */
(() => {
  'use strict';
  const sections=new Set(['home','products','categories','compare','alternatives','use-cases','guides','pricing','about','privacy','terms']);
  const events=new Set(['page_view','product_view','category_view','comparison_view','alternative_view','guide_view','pricing_view','tool_search','filter_use','compare_add','tool_finder_start','tool_finder_complete','whatsapp_click','product_whatsapp_click','outbound_vendor_click']);
  const ids=new Set(['chatgpt','gemini','veo','leonardo','elevenlabs','canva','figma','capcut','adobe','lovable','gamma','replit','n8n','notion','nordvpn','surfshark','youtube','netflix','linkedin','windows']);
  const canonical=document.querySelector('link[rel="canonical"]');
  const path=canonical ? new URL(canonical.href).pathname : '/404.html';
  const section=path.split('/').filter(Boolean)[0]||'home';
  const emit=(name,extra={})=>{
    if(!events.has(name))return;
    const detail={name,page:path,section:sections.has(section)?section:'other'};
    if(ids.has(extra.product))detail.product=extra.product;
    document.dispatchEvent(new CustomEvent('aitz:measure',{detail}));
  };
  window.aitzMeasure=emit;
  emit('page_view');
  const pageEvents={products:'product_view',categories:'category_view',compare:'comparison_view',alternatives:'alternative_view',guides:'guide_view',pricing:'pricing_view'};
  if(pageEvents[section]&&(path.split('/').filter(Boolean).length>1||section==='pricing'))emit(pageEvents[section],{product:document.querySelector('.buy-now[data-product-id]')?.dataset.productId});
  document.addEventListener('click',event=>{
    const link=event.target.closest('a[href]');
    if(link){
      const url=new URL(link.href,location.href);
      if((url.hostname==='wa.me'&&url.pathname==='/923430173923')||(url.hostname==='web.whatsapp.com'&&url.pathname==='/send/'&&url.searchParams.get('phone')==='923430173923')){
        const product=link.dataset.productId||link.dataset.waProduct;
        emit('whatsapp_click',{product});
        if(ids.has(product))emit('product_whatsapp_click',{product});
      } else if(link.matches('main a[target="_blank"]')&&url.protocol==='https:'&&url.origin!==location.origin)emit('outbound_vendor_click');
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
