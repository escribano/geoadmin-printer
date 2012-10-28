var page = require('webpage').create(),
system = require('system'),
address,outfile,width,
height,clip_height,clip_width;

if (system.args.length < 3 || system.args.length > 5) {
    console.log('Usage: screenshot.js URL filename [width height]');
    phantom.exit(1);

} else {

    address = system.args[1];
    outfile = system.args[2];
    clip_width = 600;
    clip_height = 400;
    if (system.args.length == 5) {
        clip_width = parseInt(system.args[3]);
        clip_height = parseInt(system.args[4]);
    }
}
// clipping parameter to remove map.geo.adminc
left = 300;
top = 150;
bottom = 24 + 24;

width = clip_width + left;
height = clip_height + top + bottom;

page.viewportSize = {
    width: width,
    height: height
};
page.clipRect = {
    top: top,
    left: left,
    width: clip_width,
    height: clip_height
};

page.open(address, function(status) {
    if (status !== 'success') {
        phantom.exit(1);
    } else {
        page.evaluate(function() {
            try {
                console.log('hidding');

                document.getElementById('side-panel').style.display = 'none';
                document.getElementById('header').style.display = 'none';
                document.getElementsByClassName('x-panel-tbar-noheader')[0].style.display = 'none';
                document.getElementsByClassName('x-panel-tbar-noheader')[1].style.display = 'none';
                document.getElementsByClassName('x-panel-bbar')[0].style.display = 'none';

                document.getElementsByClassName('olControlPanZoomBar')[0].style.display = "none";
                document.getElementsByClassName('olControlOverviewMap')[0].style.display = "none";
                document.getElementsByClassName('olControlPanel')[0].style.display = "none";
                /*    var p = document.getElementsByClassName('geoadmin-mappanel')[0];
                p.style.top = 0;
                p.style.left = 0;
                p.style.width = width+"px";
                p.style.height = height+"px";*/

                } catch(e) {
                console.log('error');

            }
        });
        page.render(outfile);
        phantom.exit();
    }
});