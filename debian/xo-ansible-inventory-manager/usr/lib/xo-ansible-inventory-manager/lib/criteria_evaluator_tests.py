import unittest
from criteria_evaluator import CriteriaEvaluator
from criteria_token import Token
from definitions import TokenType, OperatorType

class TestCriteriaEvaluator(unittest.TestCase):
    def setUp(self):
        # Sample host variables data
        self.host_vars = {
                'host1': {'app': 'proxmox', 'type': 'bare-metal', 'ansible_host': '10.100.4.100', 'deprecated': None, "property_2": "lol"},
                'host2': {'app': 'kubernetes', 'type': 'vm', 'ansible_host': '10.100.4.101', 'deprecated': 'no', "property_2": None},
                'host3': {'app': 'proxmox', 'type': 'lxc', 'ansible_host': '10.100.4.102', 'deprecated': None},
                'host4': {'app': 'docker', 'type': 'bare-metal', 'ansible_host': '10.100.4.200', 'deprecated': 'yes'},
                'host5': {'app': 'kubernetes', 'type': 'bare-metal', 'ansible_host': '10.100.4.201', 'deprecated': None},
                'host6': {'app': 'proxmox', 'type': 'vm', 'ansible_host': '10.100.4.202', 'deprecated': 'no'},
                'host7': {'app': 'docker', 'type': 'lxc', 'ansible_host': '10.100.4.203', 'deprecated': 'yes'}
        }


        # Sample group variables data
        self.group_vars = {
                # Logical Operators
                'group1': {'group_criteria': 'app=proxmox && type=bare-metal',
                        'expected_hosts': ['host1'],
                        'message': 'Testing logical AND operator with app=proxmox && type=bare-metal'},
                'group2': {'group_criteria': 'app=kubernetes || type=vm',
                        'expected_hosts': ['host2', 'host5', 'host6'],
                        'message': 'Testing logical OR operator with app=kubernetes || type=vm'},
                'group3': {'group_criteria': '(app=proxmox && type=lxc) || ansible_host="10.100.4.100"',
                        'expected_hosts': ['host1', 'host3'],
                        'message': 'Testing nested logical operators with (app=proxmox && type=lxc) || ansible_host="10.100.4.100"'},
                'group14': {'group_criteria': 'app="proxmox" OR app="kubernetes"',
                                'expected_hosts': ['host1', 'host2', 'host3', 'host5', 'host6'],
                                'message': 'Testing logical OR operator with app="proxmox" OR app="kubernetes"'},

                # Negated Logical Operators
                'group15': {'group_criteria': 'NOT (app=proxmox && type=bare-metal)',
                                'expected_hosts': ['host2', 'host3', 'host4', 'host5', 'host6', 'host7'],
                                'message': 'Testing negated logical AND operator with NOT (app=proxmox && type=bare-metal)'},
                'group16': {'group_criteria': 'NOT (app=kubernetes || type=vm)',
                                'expected_hosts': ['host1', 'host3', 'host4', 'host7'],
                                'message': 'Testing negated logical OR operator with NOT (app=kubernetes || type=vm)'},
                'group17': {'group_criteria': 'NOT ((app=proxmox && type=lxc) || ansible_host="10.100.4.100")',
                                'expected_hosts': ['host2', 'host4', 'host5', 'host6', 'host7'],
                                'message': 'Testing negated nested logical operators with NOT ((app=proxmox && type=lxc) || ansible_host="10.100.4.100")'},
                'group18': {'group_criteria': 'NOT (app="proxmox" OR app="kubernetes")',
                                'expected_hosts': ['host4', 'host7'],
                                'message': 'Testing negated logical OR operator with NOT (app="proxmox" OR app="kubernetes")'},

                # Comparison Operators
                'group4': {'group_criteria': 'app=proxmox && ansible_host="10.100.4.100"',
                        'expected_hosts': ['host1'],
                        'message': 'Testing comparison operator with app=proxmox && ansible_host="10.100.4.100"'},
                'group5': {'group_criteria': 'type=bare-metal',
                        'expected_hosts': ['host1', 'host4', 'host5'],
                        'message': 'Testing value parsing with type=bare-metal'},
                'group6': {'group_criteria': 'ansible_host="10.100.4.100"',
                        'expected_hosts': ['host1'],
                        'message': 'Testing quotes handling with ansible_host="10.100.4.100"'},
                'group9': {'group_criteria': 'app=proxmox',
                        'expected_hosts': ['host1', 'host3', 'host6'],
                        'message': 'Testing single condition matching hosts with app=proxmox'},
                'group10': {'group_criteria': 'app!=proxmox',
                                'expected_hosts': ['host2', 'host4', 'host5', 'host7'],
                                'message': 'Testing single condition matching hosts with app!=proxmox'},

                # Negated Comparison Operators
                'group19': {'group_criteria': 'NOT (app=proxmox && ansible_host="10.100.4.100")',
                                'expected_hosts': ['host2', 'host3', 'host4', 'host5', 'host6', 'host7'],
                                'message': 'Testing negated comparison operator with NOT (app=proxmox && ansible_host="10.100.4.100")'},
                'group20': {'group_criteria': 'NOT (type=bare-metal)',
                                'expected_hosts': ['host2', 'host3', 'host6', 'host7'],
                                'message': 'Testing negated value parsing with NOT (type=bare-metal)'},
                'group21': {'group_criteria': 'NOT (ansible_host="10.100.4.100")',
                                'expected_hosts': ['host2', 'host3', 'host4', 'host5', 'host6', 'host7'],
                                'message': 'Testing negated quotes handling with NOT (ansible_host="10.100.4.100")'},
                'group22': {'group_criteria': 'NOT (app=proxmox)',
                                'expected_hosts': ['host2', 'host4', 'host5', 'host7'],
                                'message': 'Testing negated single condition matching hosts with NOT (app=proxmox)'},
                'group23': {'group_criteria': 'NOT (app!=proxmox)',
                                'expected_hosts': ['host1', 'host3', 'host6'],
                                'message': 'Testing negated single condition matching hosts with NOT (app!=proxmox)'},

                # ISNULL and ISNOTNULL Operators
                'group24': {'group_criteria': 'deprecated ISNULL',
                                'expected_hosts': ['host1', 'host3', 'host5'],
                                'message': 'Testing ISNULL operator with deprecated ISNULL'},
                'group25': {'group_criteria': 'property_2 ISNOTNULL',
                                'expected_hosts': ['host1'],
                                'message': 'Testing ISNOTNULL operator with deprecated ISNOTNULL'},

                # Negated ISNULL and ISNOTNULL Operators
                'group26': {'group_criteria': 'NOT (property_2 ISNULL)',
                                'expected_hosts': ['host1'],
                                'message': 'Testing negated ISNULL'},
                'group27': {'group_criteria': 'NOT (deprecated ISNOTNULL)',
                                'expected_hosts': ['host1', 'host3', 'host5'],
                                'message': 'Testing negated ISNOTNULL operator with NOT (deprecated ISNOTNULL)'},

                # # Collection Operators
                # 'group28': {'group_criteria': 'app IN ("proxmox", "kubernetes")',
                #                 'expected_hosts': ['host1', 'host2', 'host3', 'host5', 'host6'],
                #                 'message': 'Testing collection IN operator with app IN ("proxmox", "kubernetes")'},
                # 'group29': {'group_criteria': 'type CMATCH "bare.*"',
                #                 'expected_hosts': ['host1', 'host4', 'host5'],
                #                 'message': 'Testing collection regex match (CMATCH) operator with type CMATCH "bare.*"'},
                # 'group30': {'group_criteria': 'app ANY ("proxmox", "kubernetes")',
                #                 'expected_hosts': ['host1', 'host2', 'host3', 'host5', 'host6'],
                #                 'message': 'Testing collection ANY operator with app ANY ("proxmox", "kubernetes")'},

                # # Negated Collection Operators
                # 'group31': {'group_criteria': 'NOT app IN ("proxmox", "kubernetes")',
                #                 'expected_hosts': ['host4', 'host7'],
                #                 'message': 'Testing NOT collection IN operator with NOT app IN ("proxmox", "kubernetes")'},
                # 'group32': {'group_criteria': 'NOT type CMATCH "bare.*"',
                #                 'expected_hosts': ['host2', 'host3', 'host6', 'host7'],
                #                 'message': 'Testing NOT collection regex match (CMATCH) operator with NOT type CMATCH "bare.*"'},
                # 'group33': {'group_criteria': 'NOT app ANY ("proxmox", "kubernetes")',
                #                 'expected_hosts': ['host4', 'host7'],
                #                 'message': 'Testing NOT collection ANY operator with NOT app ANY ("proxmox", "kubernetes")'},

                # LIKE Operator
                'group34': {'group_criteria': 'app LIKE "prox%"',
                                'expected_hosts': ['host1', 'host3', 'host6'],
                                'message': 'Testing LIKE match operator with app LIKE "prox%"'},

                # Negated LIKE Operator
                'group35': {'group_criteria': 'NOT app LIKE "prox%"',
                                'expected_hosts': ['host2', 'host4', 'host5', 'host7'],
                                'message': 'Testing NOT LIKE match operator with NOT app LIKE "prox%"'},

                # Regex Match Operators
                'group36': {'group_criteria': 'ansible_host MATCH "^10\\.100\\.4\\.1.*$"',
                                'expected_hosts': ['host1', 'host2', 'host3'],
                                'message': 'Testing regex match (MATCH) operator with ansible_host MATCH "^10\\\\.100\\\\.4\\\\.1.*$"'},

                # Negated Regex Match Operators
                'group37': {'group_criteria': 'NOT ansible_host MATCH "^10\\.100\\.4\\.1.*$"',
                                'expected_hosts': ['host4', 'host5', 'host6', 'host7'],
                                'message': 'Testing NOT regex match (MATCH) operator with NOT ansible_host MATCH "^10\\\\.100\\\\.4\\\\.1.*$"'},

                # Invalid Criteria
                'group7': {'group_criteria': 'app=invalid',
                        'expected_hosts': [],
                        'message': 'Testing invalid criteria with app=invalid'}
        }

        
        self.criteria_evaluator = CriteriaEvaluator(self.host_vars, self.group_vars, 'group_criteria')

    def test_shunting_yard_basic(self):
        tokens = [
            Token('app', TokenType.VARIABLE),
            Token('=', TokenType.COMPARISON_OPERATOR, OperatorType.EQUAL),
            Token('proxmox', TokenType.CONSTANT),
            Token('&&', TokenType.LOGICAL_OPERATOR, OperatorType.AND),
            Token('type', TokenType.VARIABLE),
            Token('=', TokenType.COMPARISON_OPERATOR, OperatorType.EQUAL),
            Token('bare-metal', TokenType.CONSTANT)
        ]
        expected_output = [
            Token('app', TokenType.VARIABLE),
            Token('proxmox', TokenType.CONSTANT),
            Token('=', TokenType.COMPARISON_OPERATOR, OperatorType.EQUAL),
            Token('type', TokenType.VARIABLE),
            Token('bare-metal', TokenType.CONSTANT),
            Token('=', TokenType.COMPARISON_OPERATOR, OperatorType.EQUAL),
            Token('&&', TokenType.LOGICAL_OPERATOR, OperatorType.AND)
        ]
        output = self.criteria_evaluator.shunting_yard(tokens)
        self.assertEqual(output, expected_output)

    def test_group_criteria(self):
        for group_name, group_data in self.group_vars.items():
            with self.subTest(f"{group_name}: group_data['message']"):
                actual_matching_hosts = [host for host in self.host_vars if self.criteria_evaluator.evaluate_criteria(group_data['group_criteria'], host)]
                expected_hosts = group_data['expected_hosts']
                
                self.assertEqual(sorted(expected_hosts), sorted(actual_matching_hosts),
                                 f"TEST: {group_name}: Expected hosts '{expected_hosts}', but got '{actual_matching_hosts}' for group '{group_name}' with criteria '{group_data['group_criteria']}'.")

if __name__ == '__main__':
    unittest.main(failfast=True)
    #unittest.main()
