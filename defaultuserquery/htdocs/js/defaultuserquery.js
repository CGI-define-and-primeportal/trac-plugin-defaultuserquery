jQuery(document).ready(function($) {

  // Find all standard query links ('/project1/query')
  var query_links = $('a[href="' + standard_query_href + '"]')
  // Replace standard query links with the default query selected by the user.
  // This should preferably have been done with a Transformer but that doesn't
  // affect the link in the ribbon.
  query_links.attr('href', replacement_query_href);

  // Replace the action of the ribbon link for choosing a default query with an
  // ajax call
  $('#make-query-default').click(function(event) {
    event.preventDefault()
    // This should be a POST, but that fails due to missing or invalid
    // form_token
    result = $.get($(this).attr('href') + window.location.search);
    // Replace query links on the page to reflect the changed default user
    // query
    query_links.attr('href', standard_query_href + window.location.search);
    // Provide user feedback
    $(this).effect("highlight", {}, 1000);
  });

});
