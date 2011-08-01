// ----------------------------------------------------------------------------
// markItUp!
// ----------------------------------------------------------------------------
// Copyright (C) 2008 Jay Salvat
// http://markitup.jaysalvat.com/
// ----------------------------------------------------------------------------
// Wikicreole by Bruno Michel
// http://github.com/nono/markitup-wikicreole/tree/master
// ----------------------------------------------------------------------------
// Wikicreole
// http://www.wikicreole.org/
// -------------------------------------------------------------------
var mySettings = {
  previewParserPath: '/2011/markitup/preview/',
  onShiftEnter: {keepDefault: false, replaceWith: '\\\\'},
  onCtrlEnter: {keepDefault: false, replaceWith: '\n\n'},
  markupSet: [
    {name:'Heading 1', key:'1', openWith:'= ', closeWith:' =', className:'h1', placeHolder:'Your title here...' },
    {name:'Heading 2', key:'2', openWith:'== ', closeWith:' ==', className:'h2', placeHolder:'Your title here...' },
    {name:'Heading 3', key:'3', openWith:'=== ', closeWith:' ===', className:'h3', placeHolder:'Your title here...' },
    {name:'Heading 4', key:'4', openWith:'==== ', closeWith:' ====', className:'h4', placeHolder:'Your title here...' },
    {separator:'---------------' },
    {name:'Bold', key:'B', openWith:'**', closeWith:'**', className:'bold', placeHolder:'Your text here...'},
    {name:'Italic', key:'I', openWith:'//', closeWith:'//', className:'italic', placeHolder:'Your text here...'},
    {separator:'---------------' },
    {name:'Bulleted list', openWith:'* ', className:'list-bullet'},
    {name:'Numeric list', openWith:'# ', className:'list-numeric'},
    {separator:'---------------' },
    {name:'Picture', key:"P", replaceWith:'{{[![Url:!:http://]!]|[![Alternative text]!]}}', className:'image'},
    {name:'Link', key:"L", replaceWith:'[[[![Url:!:http://]!]|[![Title]!]]]', className:'link'},
    {separator:'---------------' },
    {name:'Code block', openWith:'{{{', closeWith:'}}}', className:'code'},
    {name:'Preview', className:'preview', call:'preview'}
  ]
};

