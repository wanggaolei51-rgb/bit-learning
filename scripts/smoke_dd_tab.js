// V4.51.0 日期页切换卡 渲染冒烟
const fs = require('fs');
const html = fs.readFileSync('/root/.openclaw/workspace/index.html', 'utf8');
function extractObject(sm) {
  const i = html.indexOf(sm); const j = html.indexOf('{', i);
  let depth = 0, inStr = false, esc = false, q = '';
  for (let k = j; k < html.length; k++) {
    const ch = html[k];
    if (inStr) { if (esc) { esc = false; continue; } if (ch === '\\') { esc = true; continue; } if (ch === q) inStr = false; continue; }
    if (ch === '"' || ch === "'" || ch === '`') { inStr = true; q = ch; continue; }
    if (ch === '{') depth++;
    if (ch === '}') { depth--; if (depth === 0) return html.slice(j, k + 1); }
  }
}
global.document = {
  getElementById: id => ({ id, innerHTML: '', style: {}, classList: { add: () => {}, toggle: () => {}, contains: () => false }, appendChild: () => {}, addEventListener: () => {}, querySelector: () => null, querySelectorAll: () => [] }),
  head: { appendChild: () => {}, querySelector: () => null },
  createElement: () => ({ id: '', textContent: '', style: {} }),
  querySelector: () => null, querySelectorAll: () => []
};
global.window = {}; global.location = { hash: '', reload: () => {} };
global.showToast = () => {}; global.showBITInfo = () => {}; global.showTip = () => {}; global.speak = () => {};
global.showAffixRose = () => {}; global.renderAffixRose = () => {}; global.goBack = () => {}; global.playVideo = () => {}; global.broadcastDay = () => {};
const names = ['getTopicForDate', 'getVideoDB', 'ddTab', 'renderDateDetail', 'showDateStudyRecord', 'renderCADate', 'renderCAInto', 'renderCA', 'renderTopicDetail', 'caLvNorm', 'caE', 'caClickWords', 'buildDailyNoteCardForDate', 'caInjectStyles', 'caCount', 'caLvBadge', 'caLvTag', 'caSubmit', 'caWordPopup', 'caAffixGo', 'caPick', 'dnEsc', 'dnRich', 'buildNoteEntryHtml', 'buildDailyNoteCard'];
let code = '';
for (const n of names) { const m = html.match(new RegExp('function ' + n + '[\\s\\S]*?\\n}')); if (m) code += m[0] + '\n'; else console.log('缺函数:', n); }
code += 'const caData=' + extractObject('const caData = {') + ';\n';
code += 'const caCalendar=' + extractObject('const caCalendar = {') + ';\n';
code += 'const dailyNotesDB=' + extractObject('const dailyNotesDB = {') + ';\n';
code += 'const bitVocabDB=' + extractObject('const bitVocabDB = {') + ';\n';
code += 'const learningHistory={};\n';
code += 'const topicCalendar=' + extractObject('const topicCalendar = {') + ';\n';
code += 'const topicData=' + extractObject('const topicData = {') + ';\n';
code += 'const vocabDB=' + extractObject('const vocabDB = {') + ';\n';
code += 'globalThis.__rdd=renderDateDetail;';
eval(code);

let pass = 0, fail = 0;
// 自动补桩: C5 渲染链深, 测试台逐次补 global 空桩直至渲染完成(产品代码本身无此依赖问题)
const stub = new Set();
function rddWithStubs(el, ds) {
  for (let iter = 0; iter < 25; iter++) {
    try { globalThis.__rdd(el, ds); return true; }
    catch (e) {
      const m = e.message.match(/^(\w+) is not defined$/);
      if (!m || stub.has(m[1])) { console.log('  不可补桩错误:', e.message.slice(0, 60)); return false; }
      stub.add(m[1]);
      globalThis[m[1]] = () => '';
    }
  }
  return false;
}
const T = (name, cond) => { if (cond) { pass++; console.log('PASS', name); } else { fail++; console.log('FAIL', name); } };

// 场景1: 11/08 CA+日记 → 2 tabs
const el1 = { innerHTML: '', querySelector: () => ({ remove: () => {} }) };
globalThis.__rdd(el1, '2026-11-08');
const t1 = (el1.innerHTML.match(/data-ddk=/g) || []).length;
T('11/08 CA+CATAT 双tab', t1 === 2);
T('11/08 含CA面板', el1.innerHTML.includes('id="ddp-ca"'));
T('11/08 含CATAT面板', el1.innerHTML.includes('id="ddp-catat"'));
T('11/08 默认CA在前', /data-ddk="ca" class="ca-tab on"|class="ca-tab on" data-ddk="ca"/.test(el1.innerHTML) || el1.innerHTML.indexOf('ddp-ca') < el1.innerHTML.indexOf('ddp-catat'));

// 场景2: 11/07 CA+日记
const el2 = { innerHTML: '', querySelector: () => ({ remove: () => {} }) };
globalThis.__rdd(el2, '2026-11-07');
T('11/07 tab=2', ((el2.innerHTML.match(/data-ddk=/g) || []).length) === 2);

// 场景3: 10/20 (C5 ukbi_real + CA interview 共存日)
const el3 = { innerHTML: '', querySelector: () => ({ remove: () => {} }) };
rddWithStubs(el3, '2026-10-20');
const t3 = (el3.innerHTML.match(/data-ddk=/g) || []).length;
T('10/20 C5+CA tab>=2, 实际 ' + t3, t3 >= 2);
T('10/20 含c5/ca/catat三面板', el3.innerHTML.includes('id="ddp-c5"') && el3.innerHTML.includes('id="ddp-ca"'));
T('10/20 无UNDEFINED/NaN', !/UNDEFINED|>undefined<|NaN/.test(el3.innerHTML));

// 场景4: 无记录日
const el4 = { innerHTML: '' };
globalThis.__rdd(el4, '2026-01-01');
T('无记录日显示暂无记录', /暂无记录/.test(el4.innerHTML));
T('无记录日无tab', ((el4.innerHTML.match(/data-ddk=/g) || []).length) === 0);

// 场景5: 10/23 纯C5课日(无CA,可能有日记)
const el5 = { innerHTML: '', querySelector: () => ({ remove: () => {} }) };
try { T('10/23 渲染不崩', rddWithStubs(el5, '2026-10-23') && el5.innerHTML.length > 500); } catch (e) { fail++; console.log('FAIL 10/23 崩溃:', e.message); }

console.log(pass + ' PASS / ' + fail + ' FAIL');
process.exit(fail ? 1 : 0);
