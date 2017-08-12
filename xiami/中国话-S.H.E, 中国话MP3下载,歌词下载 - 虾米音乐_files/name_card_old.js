
if (XM == null) {
	var XM = {};
};

XM.NameCard = function() {
	var self = this;

	self.$win = null;			// 窗体
	self.$triggerList = [];		// 触发名片的节点
	self.$card = null;			// 名片容器
	self.$cardContent = null	// 名片内容容器
	self.cardTemplate = ''		// 名片内容模板
	self.myCardTemplate = ''	// 自己的名片内容模板
	self.dataList = {};			// 本页名片数据缓存
	self.apiUrl = '/relation/card'; // '?user_id=123'
	self.showDelay = 300;			// 延时响应
	self.hideDelay = 500;		// 延时隐藏
	// 延时隐藏时间必须大于延时响应时间
	self.hideDelay = (self.hideDelay <= self.showDelay) ? self.showDelay + 100 : self.hideDelay;
	self.isLocked = false;		// 名片的显示锁定

	self.winSize = {			// 窗口大小
		width : 0, height : 0
	};
	self.winScroll = {			// 窗口滚动距离
		left : 0, top : 0
	};
	self.cardSize = {			// 名片的尺寸
		width : 0, height : 0
	};
	self.cardPosition = {		// 名片的位置（相对于Document左上角）
		left : 0, top : 0
	};
	self.cardOffset = {			// 名片的偏移位置（相对于触发对象）
		left : 30, right : 30, top : 10, bottom : 3
	};
	self.trigerSize = {			// 触发对象的尺寸
		width : 0, height : 0
	};
	self.trigerPosition = {		// 触发对象的位置（相对于Document左上角）
		left : 0, top : 0
	};
};

XM.NameCard.prototype = {
	init : function(opt) {
		var self = this;
		
		self.showDelay = opt.showDelay || self.showDelay;
		self.hideDelay = opt.hideDelay || self.hideDelay;
		self.$win = $(window);
		self.winSize = {
			width : self.$win.width(),
			height : self.$win.height()
		};
		self.winScroll = {
			left : self.$win.scrollLeft(),
			top : self.$win.scrollTop()
		};

		self.$win.resize(function(evt) {
			self.winSize = {
				width : self.$win.width(),
				height : self.$win.height()
			};
		});

		self.$win.scroll(function(evt) {
			self.winScroll = {
				left : $(this).scrollLeft(),
				top : $(this).scrollTop()
			};
			// console.log('window.scroll', self.winScroll);
		});

		self.$card = $('<div class="name_card" id="name_card" style="display:none;">');
		self.$cardContent = $('<div class="content"></div>');
		self.$card.append(self.$cardContent);
		self.$card.append($('<div class="arrow"></div>'));
		$('body').append(self.$card);
		self.cardSize = {
			width : self.$card.outerWidth(),
			height : self.$card.outerHeight()
		};
		// console.log('size', self.cardSize);
		self.$card.mouseover(function(evt) {
			self.isLocked = true;
		}).mouseout(function(evt) {
			self.isLocked = false;
			self.hideCard();
		});


		self.cardTemplate = '<div class="inner">\
			<div class="user_info">\
				<div class="user_img">\
					<a target="_blank" href="http://www.xiami.com/u/${user_id}" title="${nick_name}"><img src="${avatar}" alt="${nick_name}" /></a>\
				</div>\
				<div class="info">\
					<a class="nick" target="_blank" href="http://www.xiami.com/u/${user_id}">${nick_name}</a>{{html icon}}\
					<p>{{html icon_gender}} ${province} ${city}\
					</p>\
				</div>\
			</div>\
			<div class="play_count"><span>累计播放歌曲</span>{{html listens_str}}</div>\
			<ul class="relation_info">\
				<li><a target="_blank" href="http://www.xiami.com/space/following/u/${user_id}">关注 <em>${followers}</em></a></li>\
				<li><a target="_blank" href="http://www.xiami.com/space/fans/u/${user_id}">粉丝 <em>${fans}</em></a></li>\
				<li class="last"><a target="_blank" href="http://www.xiami.com/space/lib-artist/u/${user_id}">收藏 <em>${collects}</em></a></li>\
			</ul>\
			<div class="relative">\
				{{if is_listen}}\
					<a class="btn btn_play" href="javascript:;" rel="nofollow" data-uid="${user_id}"><i class="icon icon_play"></i>跟TA听</a>\
				{{else}}\
					<a class="btn btn_play_disable" href="javascript:;" rel="nofollow" data-uid="${user_id}"><i class="icon icon_play_disable"></i>跟TA听</a>\
				{{/if}}\
				<a class="btn btn_send_pm" target="_blank" href="http://ihi.xiami.com/message/index?to_user_id=${user_id}"><i class="icon icon_msg"></i>私信</a>\
				{{if (is_fans && is_follow)}}\
					<a class="btn btn_relation" href="javascript:;" rel="nofollow" data-relation="3" data-uid="${user_id}" title="互相关注"><i class="icon icon_be_followed"></i>互相关注</a>\
				{{else (is_follow)}}\
					<a class="btn btn_relation" href="javascript:;" rel="nofollow" data-relation="2" data-uid="${user_id}" title="已关注"><i class="icon icon_following"></i>已关注</a>\
				{{else}}\
					<a class="btn btn_relation" href="javascript:;" rel="nofollow" data-relation="1" data-uid="${user_id}" title="加关注"><i class="icon icon_add_follow"></i>关注</a>\
				{{/if}}\
			</div>\
		</div>';

		self.myCardTemplate = self.cardTemplate;
		self.myCardTemplate = self.myCardTemplate.replace('/space/following/u/${user_id}', '/relation/following');
		self.myCardTemplate = self.myCardTemplate.replace('/space/fans/u/${user_id}', '/relation/fans');

		self.$triggerList = $('[' + opt.triggerType + ']');	// 获取所有带 opt.triggerType 属性的节点
		// self.$triggerList.mouseover(function(evt) {
		self.$triggerList.live('mouseover', function(evt) {
			var $item = $(this);
			var uid = $item.attr(opt.triggerType);
			self.isLocked = true;
			var timer = setTimeout(function() {
				if (self.isLocked) {
					self.trigerSize = {
						width : $item.outerWidth(),
						height : $item.outerHeight()
					};
					// console.log('item', size);
					self.trigerPosition = $item.offset();
					self.readData(uid);
					self.showCard();
				}
			}, self.showDelay);
		// }).mouseout(function(evt) {
		}).live('mouseout', function(evt) {
			self.isLocked = false;
			self.hideCard();
		});
	},

	// 从本页缓存中读取数据
	readData : function(uid) {
		var self = this;
		var data = self.dataList['uid_' + uid];

		if (data) {
			// console.log('readData:' + uid, data);
			self.initCardContent(data);
		} else {
			self.getData(uid);
		}
	},

	getData : function(uid) {
		var self = this;
		
		// console.log('getData:' + uid);
		$.ajax({
			url : self.apiUrl,
			type : 'get',
			dataType : 'json',
			data : {user_id : uid,_xiamitoken:_xiamitoken},
			success : function(rsp) {
				// console.log('getData', rsp);
				if (rsp.status == 1) {
					var data = rsp.data;
					if (data.gender == 'F') {
						data.icon_gender = '<i class="icon icon_female" title="女"></i>';
					} else if (data.gender == 'M') {
						data.icon_gender = '<i class="icon icon_male" title="男"></i>';
					} else {
						data.icon_gender = '';
					}
					data.avatar = (data.avatar == '' || data.avatar == null) ? 'http://img.xiami.net/res/img/default/usr50.gif' : ('http://img.xiami.net/' + data.avatar);
					// data.icon_mobile = '<i class="icon icon_mobile" title="手机用户"></i>';
					data.listens_str = self.getListensString(data.listens);
					self.getDataCallback(data);
				}
			}
		});
	},

	getDataCallback : function(data) {
		var self = this;

		if (!self.dataList['uid_' + data.user_id]) {
			self.dataList['uid_' + data.user_id] = data;
			self.showCard(data);
			self.initCardContent(data);
		}
	},

	showCard : function() {
		var self = this;
		var className = '';

		if (self.winSize.width - self.trigerPosition.left > self.cardSize.width) {	// 在右边显示
			className += 'r';
			self.cardPosition.left = self.trigerPosition.left - self.cardOffset.left;
		} else {	// 在左边显示
			className += 'l';
			self.cardPosition.left = self.trigerPosition.left + self.trigerSize.width - self.cardSize.width + self.cardOffset.right;
		}

		if (self.trigerPosition.top - self.winScroll.top > self.cardSize.height) {	// 在上方显示
			className += 't';
			self.cardPosition.top = self.trigerPosition.top - self.cardSize.height - self.cardOffset.top;
		} else {	// 在上方显示
			className += 'b';
			self.cardPosition.top = self.trigerPosition.top + self.trigerSize.height + self.cardOffset.bottom;
		}

		self.$card.removeClass('name_card_rt');
		self.$card.removeClass('name_card_rb');
		self.$card.removeClass('name_card_lt');
		self.$card.removeClass('name_card_lb');
		self.$card.addClass('name_card_' + className);
		self.$card.css({
			left : self.cardPosition.left,
			top : self.cardPosition.top
		});
		self.$card.fadeIn(200);
		// self.$card.css('display', '');
	},

	hideCard : function() {
		var self = this;

		var timer = setTimeout(function() {
			if (!self.isLocked) {
				self.$card.fadeOut(100);
				// self.$card.css('display', 'none');
			}
		}, self.hideDelay);
	},

	initCardContent : function(data) {
		var self = this;

		self.$cardContent.html('');
		if (data.is_self) {
			// console.log(self.myCardTemplate);
			self.$cardContent.append($.tmpl(self.myCardTemplate, data));
		} else {
			self.$cardContent.append($.tmpl(self.cardTemplate, data));
		}

		var relationButton = new XM.RelationButton();
		relationButton.init({
			button : $('#name_card .btn_relation'),
			addFollowCallback : function(rsp) {
				if (self.dataList['uid_' + rsp.uid]) {
					self.dataList['uid_' + rsp.uid] = null;
				}
			},
			delFollowCallback : function(rsp) {
				if (self.dataList['uid_' + rsp.uid]) {
					self.dataList['uid_' + rsp.uid] = null;
				}
			},
			isStopDefault : true
		});

		$('#name_card .btn_play').click(function(evt) {
			var user_id = $(this).data('uid');
			self.playFollowUid(user_id);
			self.record('play');
		});
	},

	getListensString : function(n) {
		var str = n.toString();
		for (var i = str.length; i < 7; i ++) {
			str = '0' + str;
		}
		str = str.split('');	// string to array for IE6
		var arr = [];
		for (var i = 0; i < str.length; i ++) {
			if (i == 0) {
				arr.push('<em class="first">' + str[i] + '</em>');
			} else if (i == 6) {
				arr.push('<em class="last">' + str[i] + '</em>');
			} else {
				arr.push('<em>' + str[i] + '</em>');
			}
		}
		return arr.join('');
	},

	/*
	addFollow : function(user_id) {
		var self = this;

		self.dataList['uid_' + user_id] = null;
		XM.Relation.addFollow(user_id);
	},

	delFollow : function(user_id) {
		var self = this;

		self.dataList['uid_' + user_id] = null;
		XM.Relation.delFollow(user_id);
	}
	*/

	playFollowUid : function(user_id) {
		var self = this;
		// console.log('playFollowUid', user_id, window.openPlayer);
		if (user_id > 0 && window.openPlayer) {
			openPlayer('uid=' + user_id);
		}
	},

	// 黄金令箭
	record : function(type) {
		// console.log('record', typeof goldlog, type);
		var userid = '&userid=';
		if (_xiamiuser) {
			userid += _xiamiuser.split('"')[0];
		} else {
			userid += 0;
		}
		if (typeof goldlog != 'undefined') {
			goldlog.record('/xiamipc.1.7','','module=name_card&property=name_card&type=' + type + userid, 'H46777410');
		}
	}
};


var nameCard = new XM.NameCard();

$(function() {
	if (typeof(nameCardOption) == 'undefined') {
		nameCard.init({
			triggerType : 'name_card'
		});
	}
});