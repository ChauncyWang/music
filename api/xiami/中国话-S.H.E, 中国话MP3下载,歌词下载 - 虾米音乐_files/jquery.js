/*! 2013-10-28 14:29:26 */
;$(function(){
	var _cursorUtils = {
		opened			: false,
		timer			: null,
		targetElem		: null,
		txtShadow		: "<div id='textareaShadow'></div>",
		txtShadowElem	: null,
		listWrap		: "<div></div>",
		listWrapElem	: null,
		curIndex		: 0,
		primaryStyles	: [ 'fontFamily', 'fontSize', 'fontWeight', 'fontStyle', 'letterSpacing',
							'paddingLeft', 'paddingTop', 'paddingBottom', 'paddingRight',
							'marginLeft', 'marginTop', 'marginBottom', 'marginRight',
							'borderLeftColor', 'borderTopColor', 'borderBottomColor', 'borderRightColor',
							'borderLeftStyle', 'borderTopStyle', 'borderBottomStyle', 'borderRightStyle',
							'borderLeftWidth', 'borderTopWidth', 'borderBottomWidth', 'borderRightWidth',
							'line-height', 'outline', 'width', 'height', 'overflowY', 'overflowX',
							'wordWrap', 'resize'],
		cursorPos		: {},
		get: function (textarea) {
			var rangeData = {text: "", start: 0, end: 0 };
			var html = "";
			if (textarea.setSelectionRange) { // W3C	
				textarea.focus();
				rangeData.start = textarea.selectionStart;
				rangeData.end = textarea.selectionEnd;
				rangeData.text = (rangeData.start != rangeData.end) ? textarea.value.substring(rangeData.start, rangeData.end): "";
			} else if (document.selection) { // IE
				textarea.focus();
				var i,
					oS = document.selection.createRange(),
					// Don't: oR = textarea.createTextRange()
					oR = document.body.createTextRange();
				oR.moveToElementText(textarea);
				
				rangeData.text = oS.text;
				rangeData.bookmark = oS.getBookmark();
				
				// object.moveStart(sUnit [, iCount]) 
				// Return Value: Integer that returns the number of units moved.
				for (i = 0; oR.compareEndPoints('StartToStart', oS) < 0 && oS.moveStart("character", -1) !== 0; i++) {
					// Why? You can alert(textarea.value.length)
					if (textarea.value.charAt(i) == '\r' ) {
						i++;
					}
				}
				rangeData.start = i;
				rangeData.end = rangeData.text.length + rangeData.start;
			};
			return rangeData;
		},
		set: function (JQtextareaElem, rangeData) {
			var textarea = JQtextareaElem.context;
			var oR, start, end;
			if(!rangeData) {
				//alert("You must get cursor position first.");
				return false;
			};
			textarea.focus();
			if (textarea.setSelectionRange) { // W3C
				textarea.setSelectionRange(rangeData.start, rangeData.end);
			} else if (textarea.createTextRange) { // IE
				oR = textarea.createTextRange();
				// Fixbug : ues moveToBookmark()
				// In IE, if cursor position at the end of textarea, the set function don't work
				if(textarea.value.length === rangeData.start) {
					//alert('hello')
					oR.collapse(false);
					oR.select();
				} else {
					oR.moveToBookmark(rangeData.bookmark);
					oR.select();
				};
			};
		}
	};
	var _textAreaPro = {
		uids	: "",
		url		: "",
		key		: "",
		uid		: 0,
		canAt : false,
		getHtml:function(textarea){
			var beforeHtml = '',afterHtml = '', result = '';
			var pat = /\s/g;
			_cursorUtils.cursorPos = _cursorUtils.get(textarea);
			
			//html = textarea.value.substring(0, _cursorUtils.cursorPos.end);
			beforeHtml = textarea.value.substring(0, _cursorUtils.cursorPos.end);
			var last = beforeHtml.lastIndexOf('@');
			afterHtml = textarea.value.substring(last+1);
			if(last>=0){
				this.key = beforeHtml.substring(last+1);
				if(pat.test(this.key)){
					this.key = "";
					this.canAt = false;
				}else{
					this.canAt = true;
				}
			}else{
				this.key = "";
				this.canAt = false;
			};
			try{
				result = "<span>" + beforeHtml.substring(0, last) + "</span>";
				result = result.replace(/\ /g, '<span style="white-space:pre-wrap;font-family:Tahoma,宋体;"> </span>');
				result = result.replace(/\n/g, '<br/>');
				result += "<em>@</em>";
				result += "<span type='after'>" + afterHtml + "</span>";
			}catch(e){
				typeof(console) != "undefined" && console.log(e)
			};
			return result;
		}
		,
		getAjaxList: function(){
			var getKey = this.key,
				content = "";
				if(getKey == ""){
					content = '<div id="autoSuggestList"><ul><li class="suggest_title">选择最近@的人</li>';
				}else{
					content = '<div id="autoSuggestList"><ul>'
				};
				$.ajax({
					url: _textAreaPro.url,
					type: 'GET',
					data:{ 'key':encodeURIComponent(getKey), 'uid':_textAreaPro.uid,'_xiamitoken':_xiamitoken },
					dataType: 'json',
					timeout: 10000,
					error: function(){
						typeof(console) != "undefined" && console.log("error")
					},
					success: function(data){
						_cursorUtils.curIndex = 0;
						if(data.status == 0){
							content = '<div id="autoSuggestList"><ul><li class="suggest_title">'+data.info+'</li></ul></div>';
							_cursorUtils.listWrapElem.html(content);
							_cursorUtils.listWrapElem.show();
							_cursorUtils.opened = true;
							return false;
						}
						if(data.status == 1){
							for(var i=0;i<data.data.length;i++){
								var u = data.data[i],name = u.nick_name, uid = u.id, pic = u.avatar;
								i == 0 ? content +='<li class="on" data-uid="' + uid + '" data-value="'+name+'"><img src="'+pic+'" width="24" height="24"/>'+name+'</li>' : content +='<li data-uid="' + uid + '" data-value="'+name+'"><img src="'+pic+'" width="24" height="24"/>'+name+'</li>';
							};
							content += "</ul></div>";
							_cursorUtils.listWrapElem.html(content);
							_cursorUtils.listWrapElem.show();
							_cursorUtils.opened = true;
						}
					}
				})
		}
		,
		showSuggest: function ( suggestTarget, targetElem ) {
			//if (_cursorUtils.targetElem = null ) _cursorUtils.targetElem = $(targetElem);
			var that = this,
				textHtml = that.getHtml(suggestTarget);
			if( that.canAt && _cursorUtils.targetElem ){
				var cssObj = _cursorUtils.targetElem.getStyleArr(_cursorUtils.primaryStyles);
				_cursorUtils.txtShadowElem.css(cssObj)
				_cursorUtils.txtShadowElem.html( textHtml );
				
				var cssPro = that.XY(_cursorUtils.txtShadowElem, suggestTarget );
				_cursorUtils.listWrapElem.css(cssPro);
				that.getAjaxList();
				return;
			}
			if( !that.canAt ){
				_cursorUtils.listWrapElem.hide();
				_cursorUtils.opened = false;
			}
		}
		,
		inputSuggest: function ( value, uid ){
			if(!value || !uid){
				_cursorUtils.listWrapElem.hide();
				_cursorUtils.opened = false;
				return false;
			}
			_cursorUtils.curIndex = 0;
			var that = this;
			try{
				var v		= _cursorUtils.targetElem.val(),
					v1		= v.substring(0,_cursorUtils.cursorPos.end),
					v2		= v.substring(_cursorUtils.cursorPos.end),
					last	= v1.lastIndexOf("@"),
					str 	= v2.indexOf(" "),
					v3		= v1.substring(0,last+1),
					content	= v3 + value + " " + v2;

				_cursorUtils.cursorPos.end 	 = _cursorUtils.cursorPos.end  + ( value.length - that.key.length+1 );
				_cursorUtils.cursorPos.start = _cursorUtils.cursorPos.start  + (value.length - that.key.length+1 );
				_cursorUtils.targetElem.val( content );
				_cursorUtils.set(_cursorUtils.targetElem, _cursorUtils.cursorPos );
			}catch(e){
				typeof(console) != "undefined" && console.log("inputSuggest error:", e);
			} finally {
				_cursorUtils.listWrapElem.hide();
				_cursorUtils.opened = false;
			}
			var input = _cursorUtils.targetElem.next();
				input.val() == "" ? input.val( uid ) : input.val( input.val() + "," + uid);
			//parent.relids = parent.relids == '' ? uid : parent.relids + "," + uid;
			parent.relids = input.val();
			that.uids = parent.relids;
		}
		,
		enterSuggest: function () {
			var selectLi = _cursorUtils.listWrapElem.find("li.on");
			var value	= selectLi.data("value"),
				uid		= selectLi.data("uid");
			this.inputSuggest( value , uid );
			this.key = "";
			this.canAt = false;
		},
		shortcutKey: function( key ){
			switch(key){
				case 27: 
					_cursorUtils.listWrapElem.hide();
					_cursorUtils.opened = false;
					_cursorUtils.curIndex = 0;
					break;
				case 38:
					var ulist 		= _cursorUtils.listWrapElem.find('li:not(.suggest_title)');
					var count_li	= ulist.size();
						if(_cursorUtils.curIndex <= 0 ) _cursorUtils.curIndex = count_li;
						ulist.removeClass('on');
						_cursorUtils.curIndex -= 1;
						ulist.eq(_cursorUtils.curIndex).addClass('on');
					break;
				case 40:
					var ulist 		= _cursorUtils.listWrapElem.find('li:not(.suggest_title)');
					var count_li	= ulist.size();
						ulist.removeClass('on');
						_cursorUtils.curIndex += 1;
						if(_cursorUtils.curIndex >= count_li ){_cursorUtils.curIndex = 0;}
						ulist.eq(_cursorUtils.curIndex).addClass('on');
					break;
				
			}
		}
		,
		XY: function (txtshadow, parentElem){
			var emlast = $(txtshadow).find("em:last");
			var pElem  = $(parentElem);
			if(emlast.length == 0) return false;
			var t = 20 + emlast.position().top  + pElem.offset().top - pElem.scrollTop();
			var l = 0  + emlast.position().left + pElem.offset().left;
			var pos = {
				top:t,
				left:l,
				position:"absolute",
				zIndex:10000
			}
			return pos;
		}
	}

	$.fn.autoSuggest = function(url, uid , relids){
		_textAreaPro.url = url;
		_textAreaPro.uid = uid;
		if( _cursorUtils.txtShadowElem == null){
			_cursorUtils.txtShadowElem = $(_cursorUtils.txtShadow);
			_cursorUtils.txtShadowElem.appendTo(document.body);
		};
		if( _cursorUtils.listWrapElem == null){
			_cursorUtils.listWrapElem = $(_cursorUtils.listWrap);
			_cursorUtils.listWrapElem.appendTo(document.body);
			_cursorUtils.listWrapElem.bind("click", function(event){
				event.stopPropagation();
				var li = null;
				if(event.target.nodeName == "LI"){
					li = $(event.target);
				}else{
					li = $(event.target).parent();
				}
				if(li.hasClass("suggest_title")){ return false; }
				var value = li.data("value"),
					uid = li.data("uid");
				_textAreaPro.inputSuggest( value, uid );
				
			});
			_cursorUtils.listWrapElem.bind("mousemove", function(event){
				if(event.target.nodeName != "LI") return false;
				if(event.target.className == "suggest_title") return false;
				$(event.target).addClass("on").siblings("li").removeClass("on")
			})
		};
		return this.each(function(){
			var uidInput = $("<input id='relids' type='hidden' name='relids'/>");
			if ( relids != undefined || relids != ""){
				uidInput.val(relids);
			}
			var elem	= $(this),
				myTop	= elem.position().top,
				myLeft	= elem.position().left;
			elem.after( uidInput );
			elem.bind("keydown", function(event){
				var that = this;
				if(_cursorUtils.opened && ( event.keyCode == 38 || event.keyCode == 40 || event.keyCode == 27 ) ){
					_textAreaPro.shortcutKey(event.keyCode);
					return false;
				}
				if( event.keyCode == 13 && _textAreaPro.canAt ) {
					_textAreaPro.enterSuggest(); 
					event.preventDefault();
					return false;
				};
				try{clearTimeout(_cursorUtils.timer)}catch(e){};
				_cursorUtils.timer =  setTimeout(function(){
					_textAreaPro.showSuggest( that , elem );
				},300);
			});
			elem.bind("mouseup", function(event){
				var that = this;
				_cursorUtils.targetElem = $(this);
				try{clearTimeout(_cursorUtils.timer)}catch(e){};
					_cursorUtils.timer =  setTimeout(function(){
					_textAreaPro.showSuggest( that, elem );
				},300);
			});
			elem.bind("blur", function(){
				// _cursorUtils.listWrapElem.hide();
			});
			elem.click(function(event){
				event.stopPropagation();
			});
		})
	};
	
	$.fn.extend({
		getStyleArr : function(stylesArr) {
			if (this.length == 0) return;
			var arr = {}, thiz = this.context;
			for(var i=0; i < stylesArr.length; i++ ) {
				var casName = stylesArr[i];
				var result = ""
				try{
					result = this.css( casName ) || ($.browser.msie ? thiz.currentStyle[casName] : document.defaultView.getComputedStyle(thiz, null)[casName]);
				}catch(e){};
				arr[casName] = result;
				
			};
			arr["position"] = "absolute";
			arr["left"] = this.offset().left;
			arr["top"] = this.offset().top;
			arr["opacity"] = 0;
			arr["text-align"] = "left";
			arr["zIndex"] = -1000;
			return arr;
		}
	});
	$("body").click(function(event){
		try{
			_cursorUtils.listWrapElem.hide();
			_cursorUtils.opened = false;
		}catch(e){}
	});
});