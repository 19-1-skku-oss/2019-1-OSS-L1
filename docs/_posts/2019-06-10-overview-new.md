---
layout: post
title: "OSS-Team L1"
summary: Overview of open source projects
featured-img: overviewjpg
---

# Git, Github and Pytest

## Git

* Brief History: Control Version System의 하나로 Github 서비스 이전(2005)에 *Linus Torvalds*에 의해 처음 만들어졌다.

* With Team L1:

  * We learn: 
    
    * 기본 흐름: 시작: git init, clone, pull
    
    * 중간: git add, commit, checkout, branch, reset, status, log
    
    * 마지막 및 협력: git push, merge, rebase 
  
  * We tackle:
    
    * undo commit: git rebase -i HEAD~i. It allows you to conveniently edit any previous commits, except for the root commit. 
    
    * pull request & merge: 4명의 팀원들이 하나의 깃허브 저장소에서 작업을 하면서 그에 따라 다양한 브랜치들이 생성됐고, 각자의 브랜치에서 한 작업 내용을 하나의 브랜치로 모아 작업을 통일 시키는 과정을 거쳤다. master에서 기본적으로 다 작업을 할 수도 있겠지만, 여러 사람이 공동 작업을 하다 보니 각자가 만든 브랜치에서 흔적을 남기는 것이 좋다는 의견이 나왔기 때문이다. <br>
    '영숙'의 경우 한글 정적 페이지에 번역 포스트를 업데이트하기 위해 gh-pages 브랜치에서 포스트 업데이트 작업을 하였고 이를 mjyoo 브랜치에 pull request를 요첨함으로써 최종적으로 깃허브 정적 페이지에 업데이트 되는 작업을 경험할 수 있었다. 이는 사실 바로 아래에서 다루게 될 branch/merge 작업과 유사한 작업 흐름이다.

  * We communicate & collaborate:

    * commit -m: commit message로 서로에게 간략하게 뭘했는지 남김, 세밀하게 자주 간략하게라도 뭐했는지 남기는게 여기서 중요! 

    * branch % merge: 각자 branch를 만들어, testing file을 만들기 시작했고, 나중에는 master에 합치기 시작, 여기서 conflict 충돌 해결하는 법 익힘.
    

## Github

* Brief History: *Chris Wanstrath* 외 세분에 의해 git repository를 외부에서 호스팅할 목적으로 만들어졌다.

* With Team L1:
  
  * communicate:
   <ul>
   <ul>
   <li>issues: 수시로 궁금하고 문제 해결이 필요한 부분을 issue로 올림, 총 10개가 만들어졌고, 4개를 끝마치고, 6개 해결 중..</li> 
    <br>
      <img src="{{site.url}}/assets/img/posts/issue.jpg" width="400" height="300" style="margin-left:auto;margin-right:auto;display:block" />
    <br>
   <li>Projects: 8개의 project 실시, 3개 마치고, 5개 진행 중..</li>
    <br><div style="display:block;margin: 0 auto">
      <img src="{{site.url}}/assets/img/posts/project.png" width="400" height="300" style="margin-left:auto;margin-right:auto;display:block"/></div>
    <br>
    <li>wiki: 팀 Wiki에 우리가 이번 실습에서 프로젝트를 진행하면서 다같이 작업한 흔적들이 최대한 임팩트 있게 남을 수 있도록 노력했다. 소주제별로 페이지를 생성하여 wiki페이지를 통해 우리팀에 대한 정보를 파악할 수 있게 만들었다.</li>
    <br>
      <img src="{{site.url}}/assets/img/posts/wiki.png" width="400" height="300" style="display:block;margin: 0 auto"/>
    <br>    
   <li>fork & pull request: 한국어를 위한 정적페이지를 따로 관리하기로 했을때, 기존 것을 fork 한 후 두번째 repository에서 호스팅.</li>
 </ul>
  </ul>
  
  * manage: 수많은 파일과 폴더를 Github를 통해 많은 사람들과 보다 효율적으로 관리하는 법을 익힘. 
  
  * static page with Jekyllthemes: <br>
    민종(한글 페이지 담당) : 번역한 document를 static page로 보여주는 것이 제일 접근하기 좋고 보기 편하다는 생각에 static page에도 큰 관심을 쏟았습니다.
    기본적으로 jekyll 테마를 적용 시킨 후에 처음엔 다른 open source project에 있는 document들 처럼 만드는 것을 목표로 했습니다. 기본적인 기능은 테마 자체에서 쉽게 사용할 수 있도록 구현되어 있어서 크게 어려움을 겪진 않았습니다. <br>
    우리가 만든 두개의 static page를 모두 보여주기 위해 기존에 적용되어 있던 static page는 fork 하여 다른 repo로 옮겼고, 기존에 잇는 repo에서 작업을 하고 난 후에 옮긴 repo에 pull request하는 방식으로 운용하였습니다.<br>
    
    영숙(영문 페이지 담당) : 기존에 한국어 깃헙 페이지가 적용 되어 있는 상황에서 새로운 테마를 바로 끌고 와 적용 시키는 데에 대한 두려움(?)이 있었기 때문에 일단 ruby를 활용하여 Jekyll 테마를 로컬에서 적용 시켜 볼 수 있는 기능을 사용했다. <br>
    이 때 상단 로고 및 메인 화면 배경사진 등 대략적인 페이지 레이아웃에 변화를 준 후 변경된 테마를 themes 브랜치를 생성하여 로컬에서 원격 저장소로 push하였다. 내 컴퓨터 프로그램 상에서 테마 코드에 변화를 주면 아래 보이는 스크린샷처럼 'local:...'의 주소로 웹페이지 생성이 되면서 그때 그때 페이지가 변화 되는 모습을 볼 수 있다.<br>
    <img src="{{site.url}}/assets/img/posts/theme_ruby.png" width="400" height="600" style="display:block;margin: 0 auto"/>

## Pytest

* Brief History: 보다 좋은 프로그램 만드는 것을 돕기 위한 관련된 모든 기능을 지원하는 Python testing tool.

* With Team L1: 

  * Why: 오픈소스 프로젝트 탐색기간 동안 서로의 공통된 관심사를 찾으려고 노력했고, 다양한 오픈소스 프로젝트들이 있었지만 팀원 모두가 사용할 수 있는 Python 언어를 기반으로 작업해 보자라는 취지에서 Pytest를 선택하게 됐다.
  
    
  * What: 처음에는 다들 무엇을 하는 것인지 이해하기 어려워했지만, 점차 코드를 테스팅하는 툴이라는 기본 목적에 맞게,
  
   <img src="{{site.url}}/assets/img/posts/pytest_first_one.PNG" width="400" height="300" alt="" />
         
   Pytest 첫 설치 및 실행부터,
          
   <img src="{{site.url}}/assets/img/posts/test_result.PNG" width="400" height="300" alt="" />
          
   테스팅 후 결과가 무엇을 의미하는지도 배웠고,

   각 시나리오에 따라 어떻게 테스팅을 하면 되는지도 조금씩 이해하기 시작함.
          
   <img src="{{site.url}}/assets/img/posts/pytest_issues.png" width="400" height="300" alt="" />
          
   모르겠고 어려운 부분은 본 프로젝트에 Issue를 직접 날려 Pytest 전문가로부터 바로 피드백을 받음.
    
  * Now:  영문 documentation 내용을 한국어로 번역하기 시작했고, 본 프로젝트에 이슈를 올려 피드백도 받기 시작했으며, pytest를 더 널리 알리기 위해 한국어 & 영문 정적페이지를 동시에 운영하기 시작했다. 


## 느낀점

#### * 민종 <br>  
_"지금까지 오픈소스 코드를 하고 이런 커뮤니티 활동에는 관심이 있었는데 프로젝트를 하면서 좀 더 공부해서 사람들이 많이 쓰는 프로젝트에도 직접 기여하고 싶다는 생각을 했습니다. 좋은 경험이였습니다."_ <br>

#### * 재영 <br>  
_"Git부터 시작해서 GitHub 그리고 Pytest까지, 오픈소스 프로젝트 전반에 대해서 팀원들과 같이 배울 수 있어서 즐거웠습니다. 이번 기회로 계속 더 활동할 수 있을 것 같아요! :)"_ <br> 

#### * 영숙 <br>  
_"깃허브를 다른 팀원들과 공유하면서 제대로 사용해 본 것이 처음이었는데, 생각보다 신선했고 깃허브를 배우면서 기본적인 마크다운/html까지 배울 수 있다는 점이 굉장히 즐거웠습니다."_ <br> 

#### * 형준 <br>  
_"몇년 전에 github에 대해 들었지만 자세한 내용은 잘 몰랐습니다. 이번 기회로 오픈소스 프로젝트 통해서 많이 배우고 즐거웠습니다. 좋은 경험이였다고 생각합니다!"_ <br> 
