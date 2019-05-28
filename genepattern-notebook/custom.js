/**
 * Use require.js to load the static GenePattern Notebook files
 */
require(['base/js/namespace', 'jquery'], function(Jupyter, $) {
    "use strict";

    // Rename python3.7 kernel
   $("[id='kernel-python3.7'] > a").text('Notebook');

   // Decode username
    const decode_username = (u) => decodeURIComponent(u.replace(/-/g, '%'));

    // Add username to the logout button
    const username =  (""+ window.location).split('/')[4];
    if (username) $('#logout').html( "Logout " + decode_username(username));

    // Add the help button to the header
    $("span > a.btn[href='/hub/home']").css("margin-right", "2px"); // Fix spacing
    $("#header-container").append(
        $('<span><a href="https://genepattern-notebook.org" target="_blank" class="btn btn-default btn-sm navbar-btn pull-right" style="margin-right: 4px;">Help</a></span>')
    );

	// Attach the loading screen
	const loadingScreen = function() {
	    const base_url = Jupyter.contents ? Jupyter.contents.base_url : (Jupyter.notebook_list ? Jupyter.notebook_list.base_url : Jupyter.editor.base_url);
	    const STATIC_PATH = location.origin + base_url + "nbextensions/genepattern/resources/";

		return $("<div></div>")
			.addClass("loading-screen")
			.append("Please wait while GenePattern Notebook is loading...")
			.append($("<br/><br/>"))
			.append(
				$("<img/>")
					.attr("src", STATIC_PATH + "gp-logo.png")
			);
	};

    // Add the loading screen if this is a notebook
    if (Jupyter.notebook) {
        $("body").append(loadingScreen());
    }

    // Fade the loading screen when the kernel is ready
    $([Jupyter.events]).on('kernel_ready.Kernel', function() {
        $(".loading-screen").hide("fade");
    });

    // Backup attempt to fade loading screen
    setTimeout(function () {
        $(".loading-screen").hide("fade");
    }, 5000);

    // Bug fix for rename dialog
    $("#notebook_name").click(function() {
        setTimeout(function() {
            Jupyter.keyboard_manager.register_events($(".modal-dialog input[type=text]"));
        }, 500);
    });

    console.log("GenePattern Notebook Repository code loaded.");
});
