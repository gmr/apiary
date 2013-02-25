/**
 * Return the views namespaced in views
 *
 * @since 2013-02-24
 */
define(
    "views",
    ["views/distributions",
     "views/navigation",
     "views/system",
     "views/systems"],
    function(Distributions, Navigation, System, Systems) {
      return {Distributions: Distributions,
              Navigation: Navigation,
              System: System,
              Systems: Systems};
    }
);
