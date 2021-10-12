$(document).ready(function(){
    $(".navbar form input").tooltip({placement: "bottom"});
});

$(document).ready(function() {

  $("#tablepress-1").tablesorter();
});

$(document).ready(function() {

  $("#tablepress-2").tablesorter();
});

$(document).ready(function() {

  $("table.met-sortable").find('th.sorting').each(
    function(idx, obj) {
      $(obj).click(function() {
        orderTable($(obj).data('name'));
      });
    }
  );
});

$(document).ready(function() {

  $("#tablepress-4").tablesorter();
});

$(document).ready(function() {

  $("#tablepress-5").tablesorter();
});

$(document).ready(function() {

  $("#tablepress-7").tablesorter();
});

function orderTable(columnName) {
  var newHref = setParam(window.location.href, 'page', '1');
  if (
    (newHref.indexOf('order=asc') > -1) &&
    (newHref.indexOf('column=' + columnName) > -1)
  ) {
    newHref = setParam(newHref, 'order', 'desc');
  } else {
    newHref = setParam(newHref, 'order', 'asc');
  }
  newHref = setParam(newHref, 'column', columnName);
  window.location.href = newHref;
}

function setParam(uri, key, val) {
    return uri
        .replace(
          new RegExp("([?&]" + key + "(?=[=&#]|$)[^#&]*|(?=#|$))"),
          "&" + key + "=" + encodeURIComponent(val)
        )
        .replace(/^([^?&]+)&/, "$1?");
}
