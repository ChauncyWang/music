/**
 * jquery.editbox.js v0.1
 * jQuery EditBox Plugin
 * @author huozhe3136 <huozhe3136@hotmail.com>
 * this plugin need jquery.color.js
 */
;(function($){
	$.fn.editbox = function(settings,extraSettings){
		var defaults = {
			type				: 'edit', 		//值可以是edit,re,quote,ubb的其中之一
			actPCss 			: 'editbox_act',	//按钮外层p的css
			divCss 				: 'post_item_editbox',	//最外层div的css
			textareaRows		: 4,
			textareaCols		: 60,
			onkeydown			: function(e) {
				if(e.ctrlKey&&e.keyCode==13) {
					$(this).parent().next().children('.bt_sub2').click();
				}
			},
			onkeyup	: function() {
				// $("textarea[node-type=editSuggest]").autoSuggest( "/relation/fetch", parent.uid);
			},
			saveBtnValue			: '保 存',
			cancelBtnValue			: '取 消',
			saveBtnWaitStatusValue	: '请稍候',
			saveBtnCss 				: 'bt_sub2',
			cancelBtnCss			: 'bt_cancle2',
			saveBtnWaitStatusCss	: 'bt_cancle2', 		//saveBtn等待状态的css
			markItUpSettings		: '',				//如果类型是ubb,需提供markItUp的设置变量
			afterAppend				: '',
			success	: function(data,status,o){
				var txt;
				if(data=='1'){
					alert('请先登录');txt = o.backup;
				}else if(data=='2'){
					alert('您还不是该小组的成员');txt = o.backup;
				}else if(data=='-1'){
                    alert('先歇会儿吧，您回帖过于频繁了~');
                }else{
					txt = data.replace(/\r\n/g,'<br />');
				}
				o.$wrap.hide('fast',function(){$(this).remove();});
				o.$this.show('fast');
				if(o.defaults.type=='edit' || o.defaults.type=='ubb'){
					o.$rel.html(txt).show('fast');					
				}else{
					var $p = o.defaults.type=='re' ? o.$rel.parent() : o.$rel.parent().parent().parent();
					$p.append(data);
					if(typeof(o.defaults.afterAppend)=='function'){o.defaults.afterAppend();}
					var $c = $p.children();
					var $last = $($c[$c.length-1]);
					$('a',$last).focus();
					$last.hide()
						.fadeIn('fast')
						.animate({backgroundColor:'#FFE222'},'slow')
						.animate({backgroundColor:'#ffffff'},1800); 
				}
				//重新注册事件
				$('.editbox').editbox();
				$('.rebox').editbox({type:'re',saveBtnValue:'回 复',afterAppend:o.defaults.afterAppend});
				$('.quotebox').editbox({type:'quote',saveBtnValue:'回 复',afterAppend:o.defaults.afterAppend});
				$('.ubbeditbox').editbox({type:'ubb',markItUpSettings:typeof(mySettings)=='undefined' ? '' : mySettings});				
			}			
		};
		
		$.extend(defaults, settings, extraSettings);
		
		return this.each(function(){
			$(this).unbind('click').click(function(){
				var url,rel,backup,txt;
				var $this,$wrap,$rel,$textArea,$p1,$p2,$saveBtn,$cancelBtn;
				var _relids = $(this).data("relids");
				
				$this =  $(this);
				$this.hide('fast');
				
				url = typeof($this.attr('url'))!='undefined' ? $this.attr('url') : $this.attr('href');
				rel = $this.attr('rel');
				if(rel == '' || $('#'+rel).size<1) return false;
				$rel = $('#'+rel);
				if(defaults.type=='edit'){
					backup = $rel.html();
					txt=backup.replace(/\n/gi,'');
					txt=txt.replace(/<br\s*\/?>/gi,'\n');	
					txt=txt.replace(/<[^>]*>([^<]*)<\/a>/gi,'$1');
				}else if(defaults.type=='ubb'){
					backup = $rel.text();
					txt = $.ajax({url: url,data:{_xiamitoken:_xiamitoken}, async: false}).responseText;
					var idReg = /\>\<[\d\,]*\>/gim;
					if(txt.indexOf("<") == 0 && idReg.test( txt )){
						txt = txt.substr(1);
					}
					txt = txt.replace(/\>\<[\d\,]*\>/gim,'');
					txt = txt.replace(/\[url\=[^\@]*\](\@[\S\s]*?)\[\/url\]/gm,'$1');
				}else{
					backup =$this.parent().prev().prev().children('a').html();
				}
				
				//创建textarea
				$textArea = $('<textarea/>').attr({'node-type':'editSuggest','rows':defaults.textareaRows,'cols':defaults.textareaCols,'value': (defaults.type=='edit' || defaults.type=='ubb') ? txt : ''});
				$textArea.keydown(defaults.onkeydown);
				$textArea.keyup(defaults.onkeyup);
				$p1 = $('<p/>').append($textArea);				
				$p2 = $('<p/>').attr('class',defaults.actPCss);				
				
				//确定按钮
				$saveBtn = $('<input type="button"/>')
					.attr({'value':defaults.saveBtnValue,'class':defaults.saveBtnCss})
					.appendTo($p2)
					.click(function(){
						var val = $textArea.val();
						if(val.length<1||/^\s*$/.test(val)){alert('内容不能为空');return false;};
						$(this).attr('disabled',true).val(defaults.saveBtnWaitStatusValue).addClass(defaults.saveBtnWaitStatusCss);
						
						var uidsInput = $textArea.next();
						
						var obj = {};
						obj.content = val;
						obj.relids = uidsInput.val();
						obj.type = parent.commentType;
						obj._xiamitoken = _xiamitoken;
						if(defaults.type=='quote'){obj.act='quote';}
						
						$.post(url,obj,function(data,status){
							if(typeof(defaults.success)=='function'){
								var o ={
									defaults:defaults,
									$this 	: $this,
									$wrap 	: $wrap,
									$rel	: $rel,
									backup	: backup,
									txt		: txt
								};
								defaults.success(data,status,o);
							}else{
								$wrap.hide('fast',function(){$(this).remove();});
								$this.show('fast');
								$rel.html(data.replace(/\r\n/g,'<br />')).show('fast');
							}
						});
					});
				
				//取消按钮
				$cancelBtn = $('<input type="button"/>').attr({'value':defaults.cancelBtnValue,'class':defaults.cancelBtnCss,'style':'margin-left:6px;'})
					.appendTo($p2)
					.click(function(){
						$wrap.hide('fast',function(){$(this).remove();});
						$this.show('fast');
						$rel.show('fast');
					});
					
				//最外层div
				$wrap=$('<div/>').attr({'class':defaults.divCss,'style':'display:none'}).append($p1).append($p2);
				
				//显示控制
				if(defaults.type=='edit' || defaults.type=='ubb'){
					$rel.hide('fast').after($wrap);
				}else{
					$p1.before($('<h5/>').html('回复:'+backup));//回复 额外加入一个h5
					defaults.type=='quote' ? $rel.parent().append($wrap) : $rel.after($wrap);
				}
				$wrap.show('fast',function(){
					$("textarea[node-type=editSuggest]").autoSuggest( "/relation/fetch", parent.uid , _relids);
				});
				//$wrap.show('fast');
				if(defaults.type=='ubb'){$textArea.markItUp(defaults.markItUpSettings);}
				
				//防止事件冒泡
				return false;
			});
		});
	}
})(jQuery);