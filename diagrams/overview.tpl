<?xml version="1.0" encoding="UTF-8" standalone="no"?>
%
% from random import random
% from itertools import cycle
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
% def talks(start, odd_pattern, even_pattern):
   <a xlink:href="/2016/schedule/talks/" target="_top" class="talks">
     % w = 50
     % for i, pattern in zip(range(5), cycle([odd_pattern, even_pattern])):
       % t0 = t(start)
       % for cprev, c, cnext in zip('.' + pattern, pattern, pattern[1:] + '.'):
         % h = {'3': t(0,30), '4': t(0,45), 'L': t(0,60), 'B': t(0, 30)}[c]
         % h += t(0, 5) if c.isdigit() and cprev.isdigit() else 0
         % h += t(0, 5) if c.isdigit() and cnext.isdigit() else 0
         % if c.isdigit():
           <rect x="{{i*w + 1}}" width="{{w - 2}}" y="{{t0+1}}" height="{{h-2}}" />
         % end
         % t0 += h
       % end
     % end
     <text x="{{w*5//2}}" y="{{t(1333)}}">Talks</text>
   </a>
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
% def plenary(start, end, name, slug):
%  w = 248
   <a xlink:href="/2016/events/{{slug}}/" target="_top" class="plenary">
     <rect x="1" width="{{w}}" y="{{t(start)}}" height="{{t(start, end)}}" />
     <text x="{{w//2}}" y="{{t(start) + t(start, end) // 2}}">{{name}}</text>
   </a>
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
    text.break {
     font-size: 14px;
     font-style: italic;
     font-weight: normal;
    }
    a:hover text {text-decoration: underline}
    .reticle text {font-size: 13px}
    .open-spaces rect {fill: #90E4D3}
    .open-space rect {stroke: black; fill: #7FDDC2}
    .tutorials rect, .talks rect {fill: #EEDDA0}
    .workshops rect, .expo rect {fill: #CEED9F}
    .plenary rect {fill: #FBE452}
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
  % if day in [3, 4, 5]:
  %  reticle(300, 2030)
  %  reticle(520, 2030)
  %  plenary(900, 1000, ('Welcome and ' if day == 3 else '') + 'Keynote', 'keynotes')
  %  title = 'PyLadies Auction ($)' if day == 4 else 'Dinner ($)'
  %  slug = 'charityauction' if day == 4 else 'dinners'
     <a xlink:href="/2016/events/{{slug}}/" target="_top" class="event">
       <rect x="1" width="248" y="{{t(1900)}}" height="{{t(1900,2030)}}" />
       <text x="{{267//2}}" y="{{t(1947)}}">{{ title }}</text>
     </a>
     <a xlink:href="/2016/events/openspaces/" target="_top" class="open-spaces"
        transform="translate(570, 0)" >
       % hour = t(0,60)
       <rect width="{{hour * 4}}" y="{{t(900)}}" height="{{t(900,2000)}}" />
       <text x="{{hour * 2}}" y="{{t(1430)}}">Open Spaces</text>
       <g class="open-space">
         % for i in range(2 * 4, 7 * 4) + range(8 * 4, 13 * 4):
           % if random() < .42:
             % y, x = divmod(i, 4)
             <rect x="{{hour*x}}" y="{{hour*y}}"
                   width="{{hour}}" height="{{hour}}" />
           % end
         % end
       </g>
    </a>
  % end
  % if day in [3, 4]:
  %  plenary(1740, 1840, 'Lightning Talks', '')
  %  talks(1050, '334L334B33', '333L433B43')
     <a xlink:href="/2016/events/exhibitfloor/" target="_top" class="expo"
        transform="translate(350, 0)" >
       <rect x="1" width="120" y="{{t(800)}}" height="{{t(800,1700)}}" />
       <text x="60" y="{{t(1155)}}">Expo Hall</text>
       <text x="60" y="{{t(830)}}" class="break">— Breakfast —</text>
       <text x="60" y="{{t(1030)}}" class="break">— Break —</text>
       <text x="60" y="{{t(1320)}}" class="break">— Lunch —</text>
       <text x="60" y="{{t(1610)}}" class="break">— Break —</text>
     </a>
  % elif day == 5:
  %  talks(1310, '333', '333')
     <a xlink:href="/2016/schedule/posters/list/" target="_top" class="expo"
        transform="translate(350, 0)" >
       <rect x="1" width="120" y="{{t(1000)}}" height="{{t(1000,1300)}}" />
       <text x="60" y="{{t(1050)}}">Posters and</text>
       <text x="60" y="{{t(1140)}}">Job Fair</text>
       <text x="60" y="{{t(1240)}}" class="break">— Lunch —</text>
     </a>
  %  plenary(1510, 1630, 'Keynote and Closing', '')
  %  plenary(1700, 1830, 'Introduction to Sprints', '')
  % end
</svg>
