(() => {
  'use strict';
  const canvas=document.getElementById('zone-canvas'),art=document.getElementById('hero-art'),toggle=document.getElementById('motion-toggle');
  const gl=canvas.getContext('webgl',{alpha:true,antialias:true,powerPreference:'low-power'});
  const media=matchMedia('(prefers-reduced-motion: reduce)');
  let paused=media.matches,visible=true,frame=0,last=0,time=0;
  function pauseState(){document.body.classList.toggle('paused',paused);toggle.setAttribute('aria-pressed',String(paused));toggle.setAttribute('aria-label',paused?'Play 3D animation':'Pause 3D animation');toggle.textContent=paused?'▷':'Ⅱ';}
  pauseState();
  toggle.addEventListener('click',()=>{paused=!paused;pauseState();if(!paused)start();});
  media.addEventListener('change',e=>{paused=e.matches;pauseState();if(!paused)start();});
  if(!gl){art.classList.add('no-webgl');toggle.hidden=true;return;}
  const vertex=`attribute vec3 position;attribute vec3 normal;uniform mat4 model;uniform float aspect;varying vec3 n;varying vec3 world;void main(){vec4 w=model*vec4(position,1.);world=w.xyz;n=mat3(model)*normal;vec3 p=w.xyz;p.z-=5.1;float f=2.35;gl_Position=vec4(p.x*f/aspect,p.y*f,(-p.z-0.2),-p.z);}`;
  const fragment=`precision mediump float;varying vec3 n;varying vec3 world;uniform vec3 tint;void main(){vec3 N=normalize(n),V=normalize(vec3(0.,0.,5.1)-world);vec3 L=normalize(vec3(-3.,5.,4.));vec3 L2=normalize(vec3(4.,-1.,2.));float diff=max(dot(N,L),0.);float spec=pow(max(dot(reflect(-L,N),V),0.),55.);float rim=pow(1.-max(dot(N,V),0.),3.);float fill=max(dot(N,L2),0.);float strip=pow(max(0.,dot(N,normalize(vec3(-.6,1.,.5)))),13.);vec3 color=tint*(.10+diff*.65+fill*.22)+vec3(.95,1.,.82)*spec*.95+vec3(.72,.87,.48)*rim*.45+strip*vec3(.5,.57,.4);color+=pow(max(dot(reflect(-L2,N),V),0.),90.)*.5;gl_FragColor=vec4(color,1.);}`;
  function shader(type,source){const s=gl.createShader(type);gl.shaderSource(s,source);gl.compileShader(s);if(!gl.getShaderParameter(s,gl.COMPILE_STATUS))throw Error(gl.getShaderInfoLog(s));return s;}
  let program;
  try{program=gl.createProgram();gl.attachShader(program,shader(gl.VERTEX_SHADER,vertex));gl.attachShader(program,shader(gl.FRAGMENT_SHADER,fragment));gl.linkProgram(program);if(!gl.getProgramParameter(program,gl.LINK_STATUS))throw Error('3D program failed');}catch(e){art.classList.add('no-webgl');toggle.hidden=true;return;}
  gl.useProgram(program);gl.enable(gl.DEPTH_TEST);gl.enable(gl.CULL_FACE);gl.clearColor(0,0,0,0);
  const vertices=[],normals=[],indices=[],major=100,minor=32;
  for(let i=0;i<=major;i++){const u=i/major*Math.PI*2;for(let j=0;j<=minor;j++){const v=j/minor*Math.PI*2,r=1.15+.27*Math.cos(v);vertices.push(r*Math.cos(u),r*Math.sin(u),.27*Math.sin(v));normals.push(Math.cos(v)*Math.cos(u),Math.cos(v)*Math.sin(u),Math.sin(v));}}
  for(let i=0;i<major;i++)for(let j=0;j<minor;j++){const a=i*(minor+1)+j,b=a+minor+1;indices.push(a,b,a+1,b,b+1,a+1);}
  function buffer(name,data){const b=gl.createBuffer();gl.bindBuffer(gl.ARRAY_BUFFER,b);gl.bufferData(gl.ARRAY_BUFFER,new Float32Array(data),gl.STATIC_DRAW);const loc=gl.getAttribLocation(program,name);gl.enableVertexAttribArray(loc);gl.vertexAttribPointer(loc,3,gl.FLOAT,false,0,0);}
  buffer('position',vertices);buffer('normal',normals);const ib=gl.createBuffer();gl.bindBuffer(gl.ELEMENT_ARRAY_BUFFER,ib);gl.bufferData(gl.ELEMENT_ARRAY_BUFFER,new Uint16Array(indices),gl.STATIC_DRAW);
  const model=gl.getUniformLocation(program,'model'),aspect=gl.getUniformLocation(program,'aspect'),tint=gl.getUniformLocation(program,'tint');
  function multiply(a,b){const o=new Float32Array(16);for(let c=0;c<4;c++)for(let r=0;r<4;r++)for(let k=0;k<4;k++)o[c*4+r]+=a[k*4+r]*b[c*4+k];return o;}
  function rotation(x,y,z){let c=Math.cos,s=Math.sin;return multiply(multiply([1,0,0,0,0,c(x),s(x),0,0,-s(x),c(x),0,0,0,0,1],[c(y),0,-s(y),0,0,1,0,0,s(y),0,c(y),0,0,0,0,1]),[c(z),s(z),0,0,-s(z),c(z),0,0,0,0,1,0,0,0,0,1]);}
  function draw(){const dpr=Math.min(devicePixelRatio,1.7),w=Math.round(canvas.clientWidth*dpr),h=Math.round(canvas.clientHeight*dpr);if(canvas.width!==w||canvas.height!==h){canvas.width=w;canvas.height=h;gl.viewport(0,0,w,h);}gl.clear(gl.COLOR_BUFFER_BIT|gl.DEPTH_BUFFER_BIT);gl.uniform1f(aspect,w/h);const turn=time*.00012;
    const m=rotation(.7+Math.sin(turn)*.15,.65+turn,-.62);m[12]=-.07;m[13]=.07;gl.uniformMatrix4fv(model,false,m);gl.uniform3f(tint,.73,.87,.5);gl.drawElements(gl.TRIANGLES,indices.length,gl.UNSIGNED_SHORT,0);
    const m2=rotation(1.73+Math.sin(turn)*.1,.1+turn,-.62);m2[12]=.1;m2[13]=-.03;gl.uniformMatrix4fv(model,false,m2);gl.uniform3f(tint,.54,.61,.43);gl.drawElements(gl.TRIANGLES,indices.length,gl.UNSIGNED_SHORT,0);
  }
  function animate(now){frame=0;if(document.hidden||!visible||paused){last=0;return;}if(last)time+=Math.min(now-last,40);last=now;draw();frame=requestAnimationFrame(animate);}
  function start(){if(!frame&&!paused&&visible&&!document.hidden)frame=requestAnimationFrame(animate);}
  new ResizeObserver(()=>draw()).observe(art);
  new IntersectionObserver(entries=>{visible=entries[0].isIntersecting;if(visible)start();},{threshold:.05}).observe(art);
  document.addEventListener('visibilitychange',()=>{if(!document.hidden)start();});
  art.addEventListener('pointermove',e=>{if(paused||media.matches||e.pointerType!=='mouse')return;const r=art.getBoundingClientRect();art.style.setProperty('--rx',`${-(e.clientY-r.top-r.height/2)/r.height*9}deg`);art.style.setProperty('--ry',`${(e.clientX-r.left-r.width/2)/r.width*12}deg`);});
  art.addEventListener('pointerleave',()=>{art.style.setProperty('--rx','0deg');art.style.setProperty('--ry','0deg');});
  canvas.addEventListener('webglcontextlost',e=>{e.preventDefault();paused=true;pauseState();art.classList.add('no-webgl');canvas.style.display='none';});
  draw();start();
})();
