(function(){
  var body = document.body;
  var model = (body && body.dataset.model) || 'claude';
  var modelName = (body && body.dataset.modelName) || 'Claude';
  var dataPath = (body && body.dataset.data) || ('data/' + model + '.json');
  var currentVersion = null;
  var searchState = { query: '', hits: [], active: -1 };

  function loadVersions(){
    return fetch(dataPath).then(function(response){
      if(!response.ok){ throw new Error('Unable to load ' + modelName + ' data: ' + response.status); }
      return response.json();
    });
  }

  function showLoadError(error){
    console.error(error);
    var tl = document.getElementById('timeline');
    if(tl){
      tl.innerHTML = '<div class="tl-card"><div class="tl-tag">版本数据加载失败。请通过本地 HTTP 服务打开页面。</div></div>';
    }
  }

  loadVersions().then(init).catch(showLoadError);

  function init(V){
    var COLORS = {};
    var tl = document.getElementById('timeline');
    var lastFocusBeforeReader = null;
    function esc(s){ return String(s || '').replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;'); }
    function escAttr(s){ return esc(s).replace(/"/g,'&quot;'); }
    function fallbackCopyText(text){
      var area = document.createElement('textarea');
      area.value = text;
      area.setAttribute('readonly', '');
      area.style.position = 'fixed';
      area.style.left = '-9999px';
      document.body.appendChild(area);
      area.select();
      var copied = false;
      try{
        copied = document.execCommand('copy');
      }catch(error){
        copied = false;
      }
      document.body.removeChild(area);
      return copied ? Promise.resolve() : Promise.reject(new Error('Clipboard copy failed'));
    }
    function copyText(text){
      if(navigator.clipboard && navigator.clipboard.writeText){
        return navigator.clipboard.writeText(text).catch(function(){
          return fallbackCopyText(text);
        });
      }
      return fallbackCopyText(text);
    }
    function buttonFlash(btn, label){
      if(!btn) return;
      var old = btn.textContent;
      btn.textContent = label;
      setTimeout(function(){ btn.textContent = old; }, 1100);
    }
    function copyWithFeedback(btn, text){
      copyText(text).then(function(){
        btn.removeAttribute('title');
        buttonFlash(btn, 'copied');
      }).catch(function(){
        btn.setAttribute('title', '复制失败，请手动选中文本复制。');
        buttonFlash(btn, 'copy failed');
      });
    }
    function citationText(v){
      var source = (v && v.source) || {};
      var lines = (source.quoted_lines || []).map(function(line){
        return line.label + ':' + line.start + '-' + line.end;
      }).join(', ');
      return [
        source.source_repo || 'unknown-repo',
        source.source_path || 'unknown-path',
        source.source_commit || 'unknown-commit',
        lines ? ('quoted_lines=' + lines) : 'quoted_lines=unlisted',
        source.license ? ('license=' + source.license) : ''
      ].filter(Boolean).join(' | ');
    }
    function lineHtml(line, lineNumber, query, hitCounter){
      var lower = line.toLowerCase();
      var q = query.toLowerCase();
      var out = '';
      var pos = 0;
      if(!q){
        return esc(line);
      }
      while(true){
        var idx = lower.indexOf(q, pos);
        if(idx === -1) break;
        out += esc(line.slice(pos, idx));
        var hitId = 'hit-' + hitCounter.count++;
        searchState.hits.push(hitId);
        out += '<mark class="prompt-hit" id="'+hitId+'" data-line="'+lineNumber+'">'+esc(line.slice(idx, idx + query.length))+'</mark>';
        pos = idx + query.length;
      }
      out += esc(line.slice(pos));
      return out;
    }
    function renderPrompt(prompt, query){
      var pre = document.getElementById('rdPrompt');
      var lines = String(prompt || '').split('\n');
      var hitCounter = { count: 0 };
      searchState.query = query || '';
      searchState.hits = [];
      searchState.active = -1;
      pre.innerHTML = lines.map(function(line, index){
        var n = index + 1;
        return '<span class="prompt-line" id="prompt-line-'+n+'" data-line="'+n+'">'+lineHtml(line, n, searchState.query, hitCounter)+'</span>';
      }).join('\n');
      updateSearchCount();
    }
    function updateSearchCount(){
      var count = document.getElementById('rdSearchCount');
      if(!count) return;
      if(!searchState.hits.length){
        count.textContent = '0/0';
      }else{
        count.textContent = (searchState.active + 1) + '/' + searchState.hits.length;
      }
    }
    function activateHit(nextIndex){
      if(!searchState.hits.length) return;
      if(searchState.active >= 0){
        var old = document.getElementById(searchState.hits[searchState.active]);
        if(old) old.classList.remove('is-active');
      }
      searchState.active = (nextIndex + searchState.hits.length) % searchState.hits.length;
      var hit = document.getElementById(searchState.hits[searchState.active]);
      if(hit){
        hit.classList.add('is-active');
        hit.scrollIntoView({ block: 'center' });
      }
      updateSearchCount();
    }
    function runSearch(){
      if(!currentVersion) return;
      var input = document.getElementById('rdSearch');
      var query = (input && input.value || '').trim();
      renderPrompt(currentVersion.prompt, query);
      if(searchState.hits.length){
        activateHit(0);
      }
    }
    function clearTargetLine(){
      var old = document.querySelector('.prompt-line.is-target');
      if(old) old.classList.remove('is-target');
    }
    function jumpToLine(lineNumber){
      clearTargetLine();
      var line = document.getElementById('prompt-line-' + lineNumber);
      if(line){
        line.classList.add('is-target');
        line.scrollIntoView({ block: 'center' });
      }
    }
    function renderQuotedLines(source){
      var box = document.getElementById('rdSourceLines');
      var lines = (source && source.quoted_lines) || [];
      if(!box) return;
      if(!lines.length){
        box.textContent = '待核对';
        return;
      }
      box.innerHTML = lines.map(function(line){
        return '<button type="button" data-line="'+line.start+'" title="jump to lines '+line.start+'-'+line.end+'">'+
          esc(line.label)+':'+line.start+'-'+line.end+
        '</button>';
      }).join('');
    }
    function versionCard(v, i){
      var item = document.createElement('div');
      item.className = 'tl-item';
      var nowTag = v.now ? '<span class="tl-now">当前最新</span>' : '';
      var shadow = v.now ? 'box-shadow:0 0 0 4px rgba(232,93,74,.2);' : '';
      item.innerHTML =
        '<span class="tdot" style="background:'+v.color+';'+shadow+'"></span>'+
        '<button type="button" class="tl-card" data-i="'+i+'" aria-label="查看 '+escAttr(modelName+' '+v.ver)+' 的完整 prompt 和详细分析">'+
          '<div class="tl-head"><span class="tl-ver">'+v.ver+'</span>'+
            '<span class="tl-date">'+v.date+'</span>'+nowTag+
            '<span class="tl-stat">'+v.words.toLocaleString()+' words · '+v.lines.toLocaleString()+' lines</span></div>'+
          '<div class="tl-tag">'+v.tagline+'</div>'+
          '<div class="tl-more"><span class="ic">⊕</span> 查看完整 prompt + 详细分析</div>'+
        '</button>';
      return item;
    }
    function renderTimeline(){
      var hasTracks = V.some(function(v){ return v.track; });
      if(!hasTracks){
        V.forEach(function(v, i){ tl.appendChild(versionCard(v, i)); });
        return;
      }
      var tracks = [];
      V.forEach(function(v){
        var name = v.track || 'Ungrouped';
        if(tracks.indexOf(name) === -1) tracks.push(name);
      });
      tracks.forEach(function(name){
        var group = document.createElement('section');
        group.className = 'tl-track';
        var versions = V.filter(function(v){ return (v.track || 'Ungrouped') === name; });
        group.innerHTML =
          '<div class="tl-track-head"><h3>'+esc(name)+'</h3>'+
          '<span>'+versions.length+' records</span></div>';
        versions.forEach(function(v){
          group.appendChild(versionCard(v, V.indexOf(v)));
        });
        tl.appendChild(group);
      });
    }
    renderTimeline();
    function openTimelineCard(card){
      if(!card) return;
      openReader(parseInt(card.getAttribute('data-i'),10), card);
    }
    tl.addEventListener('click', function(e){
      var c = e.target.closest('.tl-card');
      if(!c) return;
      openTimelineCard(c);
    });
    tl.addEventListener('keydown', function(e){
      var c = e.target.closest('.tl-card');
      if(!c || (e.key !== 'Enter' && e.key !== ' ')) return;
      e.preventDefault();
      openTimelineCard(c);
    });
    function readerIsOpen(){
      var ov = document.getElementById('overlay');
      return !!(ov && ov.classList.contains('on'));
    }
    function readerFocusables(){
      var ov = document.getElementById('overlay');
      if(!ov) return [];
      var selector = 'a[href], button:not([disabled]), input:not([disabled]), textarea:not([disabled]), select:not([disabled]), [tabindex]:not([tabindex="-1"])';
      return Array.prototype.slice.call(ov.querySelectorAll(selector)).filter(function(el){
        return !!(el.offsetWidth || el.offsetHeight || el.getClientRects().length);
      });
    }
    function focusReaderStart(){
      var close = document.querySelector('.rd-close');
      var reader = document.querySelector('.reader');
      if(close) close.focus();
      else if(reader) reader.focus();
    }
    window.openReader = function(i, opener){
      var v = V[i];
      var source = v.source || {};
      lastFocusBeforeReader = opener || document.activeElement;
      currentVersion = v;
      document.getElementById('rdVer').textContent = modelName + ' ' + v.ver;
      document.getElementById('rdVer').style.color = v.color;
      document.getElementById('rdDate').textContent = v.date;
      document.getElementById('rdTag').textContent = v.tagline;
      document.getElementById('rdStat').textContent = v.words.toLocaleString()+' words · '+v.lines.toLocaleString()+' lines';
      document.getElementById('rdSourceRepo').textContent = source.source_repo || '未标注';
      document.getElementById('rdSourcePath').textContent = source.source_path || '未标注';
      document.getElementById('rdSourceCommit').textContent = source.source_commit || '未标注';
      document.getElementById('rdSourceLicense').textContent = source.license || '未标注';
      document.getElementById('rdSourceNote').textContent = source.analysis_author_note || '';
      renderQuotedLines(source);
      var ana = v.analysis.map(function(a){
        return '<div class="ana-item"><div class="at">'+a[0]+'</div><div class="ab">'+a[1]+'</div></div>';
      }).join('');
      document.getElementById('rdAna').innerHTML = ana;
      var search = document.getElementById('rdSearch');
      if(search) search.value = '';
      renderPrompt(v.prompt, '');
      var ov = document.getElementById('overlay');
      ov.classList.add('on');
      document.body.classList.add('reader-open');
      ov.scrollTop = 0;
      focusReaderStart();
    };
    window.closeReader = function(){
      var ov = document.getElementById('overlay');
      if(!ov || !ov.classList.contains('on')) return;
      ov.classList.remove('on');
      document.body.classList.remove('reader-open');
      if(lastFocusBeforeReader && document.contains(lastFocusBeforeReader)){
        lastFocusBeforeReader.focus();
      }
      lastFocusBeforeReader = null;
    };
    var searchInput = document.getElementById('rdSearch');
    if(searchInput){
      searchInput.addEventListener('input', runSearch);
      searchInput.addEventListener('keydown', function(e){
        if(e.key === 'Enter'){
          e.preventDefault();
          activateHit(searchState.active + (e.shiftKey ? -1 : 1));
        }
      });
    }
    var prev = document.getElementById('rdPrevHit');
    if(prev) prev.addEventListener('click', function(){ activateHit(searchState.active - 1); });
    var next = document.getElementById('rdNextHit');
    if(next) next.addEventListener('click', function(){ activateHit(searchState.active + 1); });
    var copyPrompt = document.getElementById('rdCopyPrompt');
    if(copyPrompt){
      copyPrompt.addEventListener('click', function(){
        if(!currentVersion) return;
        copyWithFeedback(copyPrompt, currentVersion.prompt || '');
      });
    }
    var copyCitation = document.getElementById('rdCopyCitation');
    if(copyCitation){
      copyCitation.addEventListener('click', function(){
        if(!currentVersion) return;
        copyWithFeedback(copyCitation, citationText(currentVersion));
      });
    }
    var quoteBox = document.getElementById('rdSourceLines');
    if(quoteBox){
      quoteBox.addEventListener('click', function(e){
        var btn = e.target.closest('button[data-line]');
        if(!btn) return;
        jumpToLine(parseInt(btn.getAttribute('data-line'), 10));
      });
    }
    document.addEventListener('keydown', function(e){
      if(!readerIsOpen()) return;
      if(e.key === 'Escape'){
        e.preventDefault();
        closeReader();
        return;
      }
      if(e.key !== 'Tab') return;
      var focusables = readerFocusables();
      if(!focusables.length) return;
      var first = focusables[0];
      var last = focusables[focusables.length - 1];
      if(e.shiftKey && document.activeElement === first){
        e.preventDefault();
        last.focus();
      }else if(!e.shiftKey && document.activeElement === last){
        e.preventDefault();
        first.focus();
      }else if(!document.getElementById('overlay').contains(document.activeElement)){
        e.preventDefault();
        first.focus();
      }
    });
  }
})();
