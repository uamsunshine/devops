
(function () {
  'use strict';

  angular
    .module('horizon.dashboard.sysadmin.workorder.order')
    .controller('MessageModalController', MessageModalController)


  MessageModalController.$inject = [
    '$scope',
    'horizon.dashboard.sysadmin.workorder.message.MessageService',
    'horizon.framework.widgets.toast.service',
    '$location',
    '$window',
    '$rootScope',
    '$http',
   ];

    

  function MessageModalController($scope,MessageService,toastService,$location,$window,$rootScope,$http) {
    var ctrl = this;
    var orderId = angular.element("#order_id").val();
    var send_handle_user = angular.element("#send_handle_user").val();
    var send_order_user = angular.element("#send_order_user").val();
    var userid = angular.element("#userid").val();
    var orderUserId = angular.element("#orderUserId").val();
    var messageStatus = angular.element("#message_status").val();
    var files = [];
    var data_file = new FormData();
    $scope.is_confirm = false;
    $scope.is_close = false;
    $scope.is_reopen = false;
    $scope.is_auditpassed = false;
    $scope.is_repulse = false;
    $scope.is_submit = false;

    ctrl.getFile = function(e){
      $scope.$apply(function () {
        for (var i = 0; i < e.files.length; i++) {
            if (e.files[i]){                
              files.push(e.files[i]);
            }else{
              toastService.add('error',gettext('请添加文件'));
            }
        }
        ctrl.queue = files;

      });
    }
    
    ctrl.remove = function(e){
      for (var i=0;i<ctrl.queue.length;i++){
        if (ctrl.queue[i].name == e.item.name){
          ctrl.queue.splice(i,1);
        }
      }
    }


    ctrl.submit = function () {
      $scope.is_submit = true;
      for (var i in ctrl.queue){
        data_file.append('files',files[i]);
      }
      data_file.append('orderId',orderId);
      data_file.append('message',$scope.message);
      // data_file.append('status',messageStatus);
      data_file.append('error','提交出错!');
      if (userid == orderUserId){
        data_file.append('user',send_handle_user);
        data_file.append('hidestatus',1);
      }else{
        data_file.append('user',send_order_user);
        data_file.append('hidestatus',0)       
      }
      if($scope.message != undefined || $scope.message != null || ctrl.queue != undefined || ctrl.queue != null){
        var data = MessageService.sendMessage(data_file);              
        data.then(function(obj){
          $scope.is_submit = false;
          window.location.reload();
        });
      }


    }

    ctrl.confirm = function (){
      $scope.is_confirm = true;
      data_file.append('orderId',orderId);
      data_file.append('message','你的问题我已经收到,马上为你处理');
      data_file.append('status',1);
      data_file.append('error','确认出错!');
      data_file.append('user',send_order_user);
      var data = MessageService.sendMessage(data_file);
      data.then(function(obj){
        $scope.is_confirm = false;
        window.location.reload();
      });
    }

    ctrl.auditpassed = function (){
      $scope.is_auditpassed = true;
      data_file.append('orderId',orderId);
      data_file.append('message','很高兴通知你,你的工单已经审核通过');
      data_file.append('status',4);
      data_file.append('error','确认出错!');
      data_file.append('user',send_order_user);
      var data = MessageService.sendMessage(data_file);
      data.then(function(obj){
        $scope.is_auditpassed = false;
        window.location.reload();
      });
    }


    ctrl.repulse = function (){
      $scope.is_repulse = true;
      data_file.append('orderId',orderId);
      data_file.append('message','你提交的工单被打回,请提交新的工单');
      data_file.append('status',5);
      data_file.append('error','确认出错!');
      data_file.append('user',send_order_user);
      var data = MessageService.sendMessage(data_file);
      data.then(function(obj){
        $scope.is_repulse = false;
        window.location.reload();
      });
    }

    ctrl.close =function(){
      $scope.is_close = true;
      data_file.append('orderId',orderId);
      data_file.append('message','非常感谢你的协助');
      data_file.append('status',2);
      data_file.append('error','关闭出错!');
      data_file.append('user',send_handle_user);
      var data = MessageService.sendMessage(data_file);
      data.then(function(obj){
        $scope.is_close = false;
        window.location.reload();
      });
    }

    ctrl.reopen = function(){
      $scope.is_reopen = true;
      data_file.append('orderId',orderId);
      data_file.append('message','你好,请再帮我处理一下这个问题');
      data_file.append('status',0);
      data_file.append('error','开启出错!');
      data_file.append('user',send_handle_user);
      var data = MessageService.sendMessage(data_file);
      data.then(function(obj){
        $scope.is_reopen = false;
        window.location.reload();
      });
    }

    ctrl.recommit = function(){
      data_file.append('orderId',orderId);
      data_file.append('message','我已经修改好了，帮我再审核一次!');
      data_file.append('status',5);
      data_file.append('error','开启出错!');
      data_file.append('user',send_handle_user);
      var data = MessageService.sendMessage(data_file);
      data.then(function(obj){
        window.location.reload();
      });
    }

    ctrl.delete = function(){
      var data = MessageService.deleteOrder(orderId);
      data.then(function(obj){
        var url = '/sysadmin/workorder';
        window.location.href = url;
      });
    }

  }



})();
