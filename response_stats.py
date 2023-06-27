from robot.api import ExecutionResult
from robot.api import ResultVisitor
from robot.model.keyword import Keyword, Keywords
from robot.model.body import BodyItem
from datetime import datetime
import re
import csv


class RequestStatistics(ResultVisitor):
    _NAMES_REST_KW = [
        'DELETE On Session',
        'GET On Session',
        'HEAD On Session',
        'PATCH On Session',
        'POST On Session',
        'PUT On Session'
    ]
    _SUPPORTED_BODYITEM_TYPE = [
        BodyItem.KEYWORD,
        BodyItem.FOR,
        BodyItem.ITERATION,
        BodyItem.IF,
        BodyItem.IF_ELSE_ROOT,
        BodyItem.ELSE_IF,
        BodyItem.ELSE
    ]

    def __init__(self):
        self.requests_data = []

    def has_children(self, kw: Keyword):
        if not kw.body:
            return False
        return True

    def get_request_kw_details(self, kw: Keyword):
        endpoint = ""
        method_name = ""
        response_status_code = ""
        formatted_start_time = ""
        request_content_len = 0
        response_content_len = 0
        request_status = ""
        duration_till_headers_received_ms = 0
        duration_till_till_body_received_ms = 0
        try:
            request = kw.body[0]
            endpoint = re.search(r'path_url=(.*?)(\?|\s)', request.message).group(1)
            method_name = re.search(r'^(.*)?\sRequest', request.message).group(1)
            request_content_len = re.search(r'\'Content-Length\':\s\'(\d+)?\'', request.message).group(1)
        except:
            pass
        try:
            response = kw.body[1]
            response_status_code = re.search(r'status=.*?(\d+)', response.message).group(1)
            response_content_len = re.search(r'\'Content-Length\':\s\'(\d+)?\'', response.message).group(1)
            headers_received_elapsed_time = response.timestamp
            headers_received_elapsed_time = datetime.strptime(headers_received_elapsed_time, '%Y%m%d %H:%M:%S.%f')
            utc_start_time_object = datetime.strptime(kw.starttime, '%Y%m%d %H:%M:%S.%f')
            duration_till_headers_received_ms = headers_received_elapsed_time - utc_start_time_object
            duration_till_headers_received_ms = int(duration_till_headers_received_ms.total_seconds() * 1000)
        except:
            pass
        try:
            formatted_start_time = re.sub(r'^(\d{4})(\d{2})(\d{2})(.*)', r'\1-\2-\3\4', kw.starttime)
            duration_till_till_body_received_ms = kw.elapsedtime
            request_status = kw.status
        except:
            pass
        data = [endpoint, method_name, response_status_code, formatted_start_time, duration_till_headers_received_ms,
                duration_till_till_body_received_ms, request_content_len, response_content_len, request_status]
        return data

    def get_all_request_kw_data(self, kw: Keyword, REST_kw: Keywords, test_suite_name, test_case_name):
        if kw.type == BodyItem.KEYWORD and any(x in kw.name for x in REST_kw):
            data = self.get_request_kw_details(kw)
            data = [*[test_suite_name, test_case_name], *data]
            self.requests_data.append(data)
        if self.has_children(kw):
            for child in kw.body:
                if child.type in self._SUPPORTED_BODYITEM_TYPE:
                    self.get_all_request_kw_data(child, REST_kw, test_suite_name, test_case_name)
                elif child.type == BodyItem.MESSAGE:
                    continue
                else:
                    raise Exception("Custom error- A new BodyItem found i.e. {}, please handle in code".format(child.type))
        if kw.type == BodyItem.KEYWORD and kw.teardown:
            self.get_all_request_kw_data(kw.teardown, REST_kw, test_suite_name, test_case_name)
        return

    def visit_keyword(self, kw):
        kw_full_path = kw.parent.longname
        kw_type = kw.type
        test_suite_name = ''
        test_case_name = ''
        kw_full_path_split = re.split('(?<!\d)\.(?!\d)', kw_full_path)
        if kw_type == BodyItem.SETUP:
            test_case_name = "Suite Setup"
            test_suite_name = kw_full_path_split[-1]
        elif kw_type == BodyItem.TEARDOWN:
            test_case_name = "Suite Teardown"
            test_suite_name = kw_full_path_split[-1]
        elif kw_type == BodyItem.KEYWORD:
            test_case_name = kw_full_path_split[-1]
            test_suite_name = kw_full_path_split[-2]
        self.get_all_request_kw_data(kw, self._NAMES_REST_KW, test_suite_name, test_case_name)


def save_requests_statistics_to_csv(input_xml_path, output_csvpath):
    results = ExecutionResult(input_xml_path)
    requests_statistics = RequestStatistics()
    results.visit(requests_statistics)
    stats = requests_statistics.requests_data
    f = open(output_csvpath, 'w')
    writer = csv.writer(f, delimiter=";")
    headers = ["Request ID", "Test suite name", "Test case name", "Endpoint", "Method", "Status Code", "Start time",
               "Duration till headers received[ms]", "Duration till body received[ms]", "Request Body Length",
               "Response Body Length", "Request Result"]
    writer.writerow(headers)
    for id_row, row in enumerate(stats):
        row.insert(0, id_row + 1)
        writer.writerow(row)
    f.close()

if __name__ == '__main__':
    save_requests_statistics_to_csv('./output.xml', './test.csv')

    