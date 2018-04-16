
(function () {
	'use strict';

	angular
		.module('horizon.dashboard.sysadmin.workorder.field')
		.controller('WorkOrderEffModalController', WorkOrderEffModalController)


	WorkOrderEffModalController.$inject = [
		 '$scope',
		 'horizon.dashboard.sysadmin.workorder.field.EffService',
		 'horizon.framework.widgets.toast.service',
		 '$location',
		 '$window',
		 '$rootScope',
		// 'horizon.framework.widgets.echarts.pieSettings',
		'horizon.framework.widgets.echarts.rainbowBarSettings',
		'horizon.framework.widgets.echarts.myBigdataSettings',
		'horizon.framework.widgets.echarts.myLineBigdataSettings',
	 ];

		

	function WorkOrderEffModalController($scope,EffService,toastService,$location,$window,$rootScope,rainbowBarSettings,myBigdataSettings,myLineBigdataSettings) {
		var ctrl = this;

		function intData(input){
			return function(input) {
				return parseInt(input);
	       };		
		}

		function secondsToDateTime(seconds) {
			var days = Math.floor(seconds/86400);
			var hours = Math.floor((seconds % 86400) / 3600);
			var mins = Math.floor(((seconds % 86400) % 3600) / 60);
			var secs = ((seconds % 86400) % 3600) % 60;
			return (days > 0 ? days+'天' : '') + ( hours >0 ? ('00'+hours).slice(-2) +'时' : '') + ( mins > 0 ? ('00'+mins).slice(-2)+'分' : '') + ('00'+secs).slice(-2)+'秒'
		};

		function formatter(input){
			return function(input) {
				return secondsToDateTime(input);
	       };		
		}

		function show_detail(obj){
				var url = window.location.protocol+'//'+window.location.hostname+':'+window.location.port+'/sysadmin/workorder/'+obj+'/list/';
				// window.location.href=url;
				window.open(url,'_blank');
		}

		ctrl.show = function show(){
			var begintime = $("#workorder_begintime").val();
			var endtime = $("#workorder_endtime").val();
			init(begintime,endtime);
		}

		function init(begintime,endtime){
			var promise = EffService.init(begintime,endtime);
			var image_users = $("#show_users")[0];
			var userChart = echarts.init(image_users,'vintage');
			var image_workDealTime = $("#show_workDealTime")[0];
			var workDealTimeChart = echarts.init(image_workDealTime,'vintage');
			var image_work = $("#show_work")[0];
			var image_dealtime = $('#show_dealtime')[0];
			var orderDealTimeChart = echarts.init(image_dealtime,'vintage');
			var workChart = echarts.init(image_work,'vintage');
			var image_effs = $("#show_effs")[0];
			var effChart = echarts.init(image_effs,'vintage');
			var name = [];
			var value = [];
			var weekName = [];
			var weekValue = [];
			var weekDealTimeName = [];
			var weekDealTimeValue = [];
			var date = [];
			var orderData = [];
			var eff_date = [];
			var eff_data = [];
			var orderDealTime = [];
			promise.then(function(obj){
				$scope.orders = obj.data.orders;
				$scope.openorders = obj.data.openorders;
				$scope.ordereff = secondsToDateTime(obj.data.ordereff);
				$scope.effObject = obj.data.effObject;

				angular.forEach(obj.data.users,function(data){
					name.push(data.username);
					value.push(data.count);
				});

				angular.forEach(obj.data.effObject,function(data) {
					eff_date.push(data.time +' ' + secondsToDateTime(data.value));
					eff_data.push(data.value);
				});

				angular.forEach(obj.data.weekUsers,function(data){
					weekName.push(data.username);
					weekValue.push(data.count);
				});

				angular.forEach(obj.data.weekDealTime,function(data){
					weekDealTimeName.push(data.username);
					weekDealTimeValue.push(data.sum);
				});

				var effsettings = {x:eff_date, title:'每周工单处理效率',series:[{data:eff_data, name: '效率(毫秒)'}]};
				effChart.setOption(myLineBigdataSettings.option(effsettings));
				window.onresize = effChart.resize;

				var optionsettings = {formatter:intData(),name:'处理数量', data:value,date:name, title:'工单处理数量分布',subtext:'处理数量'};
				userChart.setOption(rainbowBarSettings.option(optionsettings));
				window.onresize = userChart.resize;

				var optionsettings = {formatter:intData(),name:'处理数量', data:weekValue,date:weekName, title:'每周工单处理数量分布',subtext:'处理数量'};
				workChart.setOption(rainbowBarSettings.option(optionsettings));
				window.onresize = workChart.resize;

				var optionsettings = {formatter:formatter(),name:'处理时长', data:weekDealTimeValue,date:weekDealTimeName, title:'每周工单处理时长分布',subtext:'处理时长'};
				workDealTimeChart.setOption(rainbowBarSettings.option(optionsettings));
				window.onresize = workDealTimeChart.resize;

				// angular.forEach(obj.data.ordertime,function(data){
				//   date.push('工单ID:'+data.id+' 效率:'+secondsToDateTime(data.time));
				//   orderData.push(data.time);
				// });
				// var settings = {x:date,title:'工单确认时长', series:[{data:orderData, type:'bar',name: '耗时'}]};
				// orderChart.setOption(myBigdataSettings.option(settings));
				// window.onresize = orderChart.resize;
				// orderChart.on('click', function(params){
				//   if (params.name.split(' ').length >0){
				//     if (params.name.split(' ')[0].split(':').length > 0){
				//       show_detail(params.name.split(' ')[0].split(':')[1]);            
				//     }
				//   }
				// });

				angular.forEach(obj.data.orderDealTime,function(data){
					date.push('工单ID:'+data.id+' 耗时:'+secondsToDateTime(data.time));
					orderDealTime.push(data.time);
				});
				var settings = {x:date,title:'工单处理时长', series:[{data:orderDealTime, type:'bar',name: '耗时'}]};
				orderDealTimeChart.setOption(myBigdataSettings.option(settings));
				window.onresize = orderDealTimeChart.resize;
				orderDealTimeChart.on('click', function(params){
					if (params.name.split(' ').length >0){
						if (params.name.split(' ')[0].split(':').length > 0){
							show_detail(params.name.split(' ')[0].split(':')[1]);            
						}
					}
				});

			});

		}

		init();

	}



})();
