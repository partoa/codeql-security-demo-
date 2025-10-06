/**
 * @name Command Injection Detection
 * @description Finds command injection vulnerabilities by tracking user input to system command execution
 * @kind path-problem
 * @problem.severity error
 * @precision high
 * @id py/command-injection-demo
 * @tags security
 *       external/cwe/cwe-078
 */

import python
import semmle.python.security.dataflow.CommandInjectionQuery
import DataFlow::PathGraph

from CommandInjectionConfiguration config, DataFlow::PathNode source, DataFlow::PathNode sink
where config.hasFlowPath(source, sink)
select sink.getNode(), source, sink,
  "Command injection vulnerability: user input $@ flows to system command execution",
  source.getNode(), "from here"
