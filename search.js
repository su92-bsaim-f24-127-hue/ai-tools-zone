/* Catalog-only intent matching. Query/filter state never becomes a crawlable URL. */
(() => {
  'use strict';
  const aiCategories = new Set(['AI Assistants','AI Video','Design','AI Voice','Development','Productivity']);
  const aliases = {student:'study',students:'study',teacher:'study',teachers:'study',researcher:'research',researchers:'research',developer:'code',developers:'code',coding:'code',writer:'writing',writers:'writing',designer:'design',designers:'design',images:'design',image:'design',videos:'video',youtube:'video',youtubers:'video',creator:'content',creators:'content',freelancer:'content',freelancers:'content',marketer:'content',marketers:'content',voices:'voice',audio:'voice',businesses:'business',automate:'automation'};
  const stop = new Set('i me my need want an a the for in of and with to please show find buy best affordable tool tools subscription subscriptions plan plans pakistan pkr rs'.split(' '));
  function duration(p) {
    const d=p.duration.toLowerCase();
    if (/^1 month$/.test(d)) return 'monthly';
    if (/year|^(12|18|24) months?$/.test(d)) return 'long-term';
    if (/lifetime/.test(d)) return 'lifetime';
    if (/months?$/.test(d)) return 'multi-month';
    return 'allowance';
  }
  function parse(query) {
    let q=query.toLowerCase().replace(/[,]/g,'');
    const price=q.match(/\b(under|below|up to|at most)\s*(?:pkr|rs\.?\s*)?\s*(\d+)\b/);
    const budget=price?Number(price[2]):Infinity;
    if(price)q=q.replace(price[0],'');
    const access=q.match(/\b(private|shared|invitation|license key)\b/)?.[1] || '';
    if(access)q=q.replace(access,'');
    const ai=/\bai\b/.test(q);q=q.replace(/\bai\b/g,'');
    const tokens=q.replace(/[^a-z0-9 ]/g,' ').split(/\s+/).filter(t=>t&&!stop.has(t));
    return {budget,exclusive:!!price&&['under','below'].includes(price[1]),access,ai,tokens};
  }
  function matches(p, query, filters={}) {
    const q=typeof query==='string'?parse(query):query;
    if(q.exclusive?p.price>=q.budget:p.price>q.budget)return false;
    if(q.access && p.access.toLowerCase()!==q.access)return false;
    if(q.ai && !aiCategories.has(p.category))return false;
    const hasIntent=intent=>p.intent.includes(intent)||(intent==='content'&&p.intent.includes('creator'));
    if(filters.intent && filters.intent!=='all' && !hasIntent(filters.intent))return false;
    if(filters.intent==='video' && p.category==='Entertainment')return false;
    if(filters.duration && filters.duration!=='all' && duration(p)!==filters.duration)return false;
    const text=[p.name,p.category,p.description,...p.bestFor,...p.intent].join(' ').toLowerCase();
    return q.tokens.every(t=>{
      if(t==='youtube' && q.tokens.includes('premium'))return text.includes('youtube');
      const intent=aliases[t]||t;
      if(intent==='video' && p.category==='Entertainment' && !q.tokens.includes('premium'))return false;
      return aliases[t] ? hasIntent(intent)||text.includes(t) : text.includes(t);
    });
  }
  window.CatalogSearch={parse,matches,duration};
})();
