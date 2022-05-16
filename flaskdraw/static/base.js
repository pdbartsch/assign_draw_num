// data tables defaults.  may be overridden for specific tables
$.extend($.fn.dataTable.defaults, {
  paging: false,
  scrollY: 500,
});

// apply to tables with the following ids:
$(document).ready(function () {
  $("#loc_list").DataTable({});
  $("#proj_list").DataTable({});
  $("#draws_list").DataTable({});
});
