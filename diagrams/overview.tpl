<?xml version="1.0" encoding="UTF-8" standalone="no"?>
%
% def reticle(x, end):
%  for h in range(900, end, 100):
    <g transform="translate({{x}}, {{t(h) + 0.5}})" class="reticle">
      <path d="M -40 0 L -30 0 z  M 30 0 L 40 0 z" />
      <text x="0" y="0">
        {{h//100 - (0 if h<1300 else 12)}}:00 {{'am' if h < 1200 else 'pm'}}
      </text>
    </g>
%  end
% end
%
% def tutorials(w=30, offset=143):
   <a xlink:href="/2016/schedule/tutorials/" target="_top" class="tutorials">
%  for x in range(0, w*9, w):
    <rect x="{{x+1}}" width="{{w-3}}" y="{{t(900)}}" height="{{t(900,1220)}}" />
%  end
    <text x="{{w*4.5}}" y="{{t(900+offset)}}">Morning Tutorials ($)</text>
   </a>
   <a xlink:href="/2016/schedule/tutorials/" target="_top" class="tutorials">
%  for x in range(0, w*9, w):
    <rect x="{{x+1}}" width="{{w-3}}" y="{{t(1320)}}" height="{{t(1320,1640)}}" />
%  end
    <text x="{{w*4.5}}" y="{{t(1320+offset)}}">Afternoon Tutorials ($)</text>
    <text x="{{w*4.5}}" y="{{t(1250)}}">Lunch</text>
   </a>
% end
%
% def workshops(w=55):
   <a xlink:href="/2016/schedule/sponsor-tutorials/" target="_top" class="workshops">
%  for x in range(0, w*2, w):
    <rect x="{{x+1}}" width="{{w-3}}" y="{{t(900)}}" height="{{t(900,1030)}}" />
    <rect x="{{x+1}}" width="{{w-3}}" y="{{t(1050)}}" height="{{t(1050,1220)}}" />
    <rect x="{{x+1}}" width="{{w-3}}" y="{{t(1320)}}" height="{{t(1320,1450)}}" />
    <rect x="{{x+1}}" width="{{w-3}}" y="{{t(1510)}}" height="{{t(1510,1640)}}" />
%  end
    <text x="{{w}}" y="{{t(930)}}">Sponsor</text>
    <text x="{{w}}" y="{{t(1010)}}">Workshops</text>
   </a>
   <text x="{{w}}" y="{{t(1250)}}">Lunch</text>
% end
%
% def summit(name, w=100):
   % slug = 'education-summit' if name == 'Education' else 'language-summit'
   <a xlink:href="/2016/events/{{slug}}/" target="_top" class="summit">
     <rect x="{{1}}" width="{{w-3}}" y="{{t(900)}}" height="{{t(900,1220)}}" />
     <rect x="{{1}}" width="{{w-3}}" y="{{t(1320)}}" height="{{t(1320,1640)}}" />
     <text x="{{w//2}}" y="{{t(930)}}">{{name}}</text>
     <text x="{{w//2}}" y="{{t(1010)}}">Summit</text>
   </a>
   <text x="{{w//2}}" y="{{t(1250)}}">Lunch</text>
% end
%
<svg
   xmlns="http://www.w3.org/2000/svg"
   xmlns:xlink="http://www.w3.org/1999/xlink"
   width="1000px"
   height="{{ t(t.start, t.end) }}px"
   viewBox="0 0 1000 {{ t(t.start, t.end) }}"
   >
  <style>
    path {
     stroke-width: 1px;
     stroke: black;
    }
    text {
     fill: black;
     stroke: none;
     text-anchor: middle;
     dominant-baseline: middle;
     font-family: Helvetica;
     font-size: 18px;
     font-weight: bold;
    }
    a:hover text {text-decoration: underline}
    .reticle text {font-size: 13px}
    .tutorials rect {fill: #EEDDA0}
    .workshops rect {fill: #CEED9F}
    .summit rect {fill: #D1EE3D}
    .event rect {fill: #E0E0E0}
  </style>
  % if day in [1, 2]:
  %  reticle(320, 1730 if day == 1 else 2130)
  %  tutorials()
     <g transform="translate(370, 0)">
       % workshops()
     </g>
  %  reticle(530, 1730)
     <g transform="translate(580, 0)">
       % summit('Language' if day == 1 else 'Education')
     </g>
  % end
  % if day == 2:
     <a xlink:href="/2016/events/reception/" target="_top" class="event">
       <rect x="1" width="267" y="{{t(1800)}}" height="{{t(1800,2100)}}" />
       <text x="{{267//2}}" y="{{t(1930)}}">Opening Reception</text>
     </a>
  % end
</svg>
