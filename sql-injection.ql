/**
 * @name SQL Injection Detection
 * @description Finds SQL injection vulnerabilities by tracking user input to SQL execution
 * @kind path-problem
 * @problem.severity error
 * @precision high
 * @id py/sql-injection-demo
 * @tags security
 *       external/cwe/cwe-089
 */

import python
import semmle.python.security.dataflow.SqlInjectionQuery
import DataFlow::PathGraph

from SqlInjectionConfiguration config, DataFlow::PathNode source, DataFlow::PathNode sink
where config.hasFlowPath(source, sink)
select sink.getNode(), source, sink,
  "SQL injection vulnerability: user input $@ flows to SQL execution without sanitization",
  source.getNode(), "from here"
