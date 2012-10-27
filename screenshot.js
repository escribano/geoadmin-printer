var page = new WebPage(),
    address, outfile, width, height, clip_height;
    
    //  http://map.geo.admin.ch/?Y=727770&X=163650&zoom=4&bgLayer=ch.swisstopo.pixelkarte-farbe&layers=ch.bafu.schutzgebiete-schweizerischer_nationalpark,ch.bafu.schutzgebiete-paerke_nationaler_bedeutung,ch.bafu.bundesinventare-moorlandschaften,ch.bfe.abgeltung-wasserkraftnutzung,ch.bafu.wasser-leitungen,ch.bafu.wasser-rueckgabe,ch.bafu.wasser-entnahme&layers_opacity=0.75,0.85,0.75,1,1,1,1&layers_visibility=true,true,true,true,true,true,true&lang=fr
    
    // http://s.geo.admin.ch/27498582
    
    
   // http://map.geo.admin.ch/?selectedNode=LT1_4&Y=672470&X=172050&zoom=2&bgLayer=ch.swisstopo.pixelkarte-farbe&layers=ch.bafu.wasser-leitungen,ch.bafu.wasser-rueckgabe,ch.bafu.wasser-entnahme&layers_opacity=1,1,1&layers_visibility=true,true,true&lang=fr

address = phantom.args[0];
outfile = phantom.args[1];

//height = 800;
left = 300;
top = 150;
bottom = 24;
clip_height = 400; // = height - top;
clip_width = 600; //width - left ;
width = clip_width + left;
height = clip_height + top + bottom;


page.viewportSize = { width: width, height: height };
page.clipRect = { top: top, left: left, width: clip_width, height: clip_height };
//page.paperSize = { format: 'A4', orientation: 'landscape', border: '1cm' }

page.open(address, function (status) {
  if (status !== 'success') {
    phantom.exit(1);
  } else {
    page.evaluate(function(){
           try {
	        console.log('hidding');
                document.getElementsByClassName('olControlPanZoomBar')[0].style.display = "none";
		document.getElementsByClassName('olControlOverviewMap')[0].style.display = "none";
		document.getElementsByClassName('olControlPanel')[0].style.display = "none";
                
            } catch (e) {
	      console.log('error');
               
            }
        });
    
    
    
    page.render(outfile);
    //var base64image = page.renderBase64('PNG');
    //var fs = require("fs");
    //fs.write("/dev/stdout", base64image, "w");
    phantom.exit();
  }
});
