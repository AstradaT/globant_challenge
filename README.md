[![LinkedIn][linkedin-shield]][linkedin-url]



<!-- PROJECT LOGO -->
<br />
<div align="center">
  <a href="https://github.com/AstradaT/globant_challenge">
    <img src="https://avatars.githubusercontent.com/u/42160024" alt="Logo" width="80" height="80">
  </a>

<h3 align="center">Globant Data Challenge</h3>
</div>



<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#contact">Contact</a></li>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->
## About The Project

[![Product Name Screen Shot][product-screenshot]](https://example.com)

This project consists in the creation of an SQL database to store data from csv files and an API to query the database. Also, a feature to backup the data in AVRO format and restore it.

<p align="right">(<a href="#readme-top">back to top</a>)</p>



### Built With

* [![Python][Python]][Python-url]
* [![Flask][Flask]][Flask-url]
* [![SQLite][SQLite]][SQLite-url]
* [![Docker][Docker]][Docker-url]

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- GETTING STARTED -->
## Getting Started

You need to install Docker to run this project.

### Installation

1. Clone the repo
   ```sh
   git clone https://github.com/AstradaT/globant_challenge.git
   ```
2. Build the Docker image
   ```sh
   sudo docker build -t globant-challenge .
   ```
3. Run the container
  ```sh
  sudo docker run -p 5000:5000 globant-challenge
  ```
4. Go to http://localhost:5000

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- USAGE EXAMPLES -->
## Usage

--

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- CONTACT -->
## Contact

Tomás Astrada - [LinkedIn](https://www.linkedin.com/in/tomas-astrada/) - tomasastrada907@gmail.com

Project Link: [https://github.com/AstradaT/globant_challenge](https://github.com/AstradaT/globant_challenge)

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555
[linkedin-url]: https://www.linkedin.com/in/tomas-astrada/
[product-screenshot]: images/screenshot.png
[Python]: https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white
[Python-url]: https://www.python.org/
[Flask]: https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white
[Flask-url]: https://flask.palletsprojects.com/
[SQLite]: https://img.shields.io/badge/SQLite-07405E?style=for-the-badge&logo=sqlite&logoColor=white
[SQLite-url]: https://sqlite.org/
[Docker]: https://img.shields.io/badge/Docker-0073EC?style=for-the-badge&logo=docker&logoColor=white
[Docker-url]: https://www.docker.com/
