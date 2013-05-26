//Example code for launchable applet packaged in Pyj2d_Applet.jar with separate jython.jar.


//JavaScript:

<script type="text/javascript">
function appletLauncher (appletArchive,appletCode,appletWidth,appletHeight)
{
  var appletID = appletArchive;
  var appletArchive = appletArchive + ".jar,jython.jar";
  var appletCodebase = "http://website.com/apps/";
  var appletCode = appletCode || "Applet.class";
  var appletWidth = appletWidth || "400";
  var appletHeight = appletHeight || "300";
  document.getElementById(appletID).innerHTML = '<applet width=' + appletWidth + ' height=' + appletHeight + ' codebase=' + appletCodebase + ' code=' + appletCode + ' archive=' + appletArchive + ' alt="Applet requires JVM to run">';
}
</script>


//HTML:

<div id="Pyj2d_Applet" title="Applet: Pyj2d_Applet" style="width:400px; height:300px; border:1px solid #333; background-color:#000; position:relative; left:100px;">
<input type='button' value='Launch Applet' onClick='appletLauncher("Pyj2d_Applet")'/>
<div style="position:absolute; top:138px; width:400px; font-size:24px; color:#646464; text-align:center;">Applet</div>
</div>

