# Interface_CICD

모놀로식으로 동작하는 어플리케이션을 MSA 로 마이그레이션 하면서 

총 네개의 어플리케이션으로 분리하였습니다.

현재 어플리케이션은 쿠버네티스 상에서 각각의 파드로서 배포되어 있습니다. 

변경된 어플리케이션만 새롭게 빌드되어 Kustomization 후 

Argo CD 에서 변경사항을 지켜보다 새로운 이미지 태그를 인식하고

쿠버네티스로 배포하도록 만들어 보았습니다. 

