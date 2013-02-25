/**
 * Return the namespaced models
 *
 * @since 2013-02-24
 */
define(
    "models",
    ["models/distribution",
     "models/system"],
    function(Distribution, System) {
      return {Distribution: Distribution,
              System: System};
    }
);
