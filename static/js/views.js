define([
    "apiary_tools",
    "dust",
    "tableview",
    "views/distributions",
    "views/navigation"
], function(ApiaryTools,
            dust,
            TableView,
            DistributionsView,
            NavigationView) {

    TableView.initialize();

    var templates = ["base",
                     "snippets/breadcrumbs",
                     "snippets/navigation",
                     "components/tableview",
                     "pages/dashboard"];
    ApiaryTools.compile_templates(templates);

    return {DistributionsView: DistributionsView,
            NavigationView: NavigationView};
});
