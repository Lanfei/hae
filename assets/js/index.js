(function(){

	var app;
	
	var main = function(){
		initApp();
		initEvent();
	};

	var initApp = function(){
		app = HAE.app;
		app.setMinSize(600, 500);
		app.setResizerSize(5);
		app.setResizerMargin(17);
		app.setFrameless(true);
		app.setTransBackground(true);
		app.show();
	};

	var initEvent = function(){
		var closeEvent = function(){
			app.setClosable(confirm('真的要关闭吗？'));
		};
		var stateChangeEvent = function(){
			console.log(this);
			$('#wrap').toggleClass('maximized', app.isMaximized() || app.isFullScreen());
		};
		app.addEvent({
			close: closeEvent,
			statechange: stateChangeEvent
		});
		$(window).bind({
			beforeunload: function(){
				app.removeEvent('close', closeEvent);
				app.removeEvent('statechange', stateChangeEvent);
			}
		});
		$('#header').bind({
			mousedown: function(event){
				if(event.which == 1 && ! $(event.target).is('button')){
					app.dragStart();
				}
			},
			mouseup: function(event){
				if(event.which == 1){
					app.dragStop();
				}
			},
			dblclick: function(){
				if(app.isMaximized()){
					app.normalize();
				}else{
					app.maximize();
				}
			}
		});
		$('#minimize').bind({
			click: function(){
				app.minimize();
				return false;
			}
		});
		$('#maximize').bind({
			click: function(){
				if(app.isMaximized()){
					app.normalize();
				}else{
					app.maximize();
				}
				return false;
			}
		});
		$('#close').bind({
			click: function(){
				app.close();
				return false;
			}
		});
		$('#nav').delegate('.item', {
			click: function(e){
				var index = $(this).data('index');
				if(index !== undefined && ! $(this).hasClass('item-cur')){
					var $article = $('#main .article').hide().addClass('invisible').eq(index).show();
					$('#nav .item').removeClass('item-cur');
					setTimeout(function(){
						$article.removeClass('invisible');
					});
					$(this).addClass('item-cur');
					$(this).parents('.item-parent').addClass('item-cur');
					e.stopPropagation();
				}
			}
		});
		$('#main').bind({
			scroll: function(){
				if($(this).scrollTop() > 0){
					$(this).addClass('inset-shadow');
				}else{
					$(this).removeClass('inset-shadow');
				}
			}
		});
		$('.demos a').bind({
			click: function(event){
				var href = $(this).data('href');
				if(href){
					new HAE.Window(href);
					event.preventDefault();
				}
			}
		});
	};

	main();
})();