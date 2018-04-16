(function () {
  'use strict';

  angular
    .module('horizon.dashboard.sysadmin.workorder.message')
    .factory('horizon.dashboard.sysadmin.workorder.message.MessageService', MessageService)

  MessageService.$inject = [
    '$q',
    'horizon.framework.util.http.service',
    'horizon.framework.widgets.toast.service',
    '$http',
   ];

  function MessageService($q, apiService, toastService,$http) {

    var model = {
      sendMessage:sendMessage,
      deleteOrder:deleteOrder,
    };

    function sendMessage(orderId,message,messageStatus){
      var data = JSON.stringify({'orderId':orderId,'message':message,'status':messageStatus});

      return apiService.post('/sysadmin/workorder/order/message',data)
          .error(function(obj){
            console.log(obj);
            // toastService.add('error', gettext('角色名重复'));
          });

    }

    function deleteOrder(orderId){
      var data = JSON.stringify({'orderId':orderId})
      return apiService.post('/sysadmin/workorder/order/delete',data)
            .error(function(obj){
              console.log(obj);
            });
    }

    return model;
  }

})();
