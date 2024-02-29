
# InfoJobs Apply Bot
Realiza a candidatura em vagas do infojobs a partir de parâmtros definidos em um arquivo json.

## Requisitos
- Mozilla Firefox
- Sqlite3
- Python3

## Instalação
1. Insira no terminal: python3 -m venv env
2. Insira no terminal: source ./env/bin/activate ou \env\Scripts\activate no windows
3. Insira no terminal: pip install -r requirements.txt
4. Insira no terminal: python3 setup.py

## Instruções
1. Crie um arquivo .env na raiz do projeto seguindo o exemplo do arquivo .env-example
2. Rode o código bot.py inserindo no terminal: python3 bot.py e insira algum desses comandos:
    | Comando | Descrição |
    | --- | --- |
    | /pull | baixa as urls de empregos encontrados a partir da busca definida pelo arquivo json params.json |
    | /candidate | realiza a candidatura em vagas que foram armazenadas com o comando /pull |
    | /view | descreve informações sobre os empregos que foram armazenados com o comando /pull |
    | /clear | exclui todos os empregos no banco de dados |
    | /quit | termina a execução do bot e encerra o programa |

3. Passe as informações no arquivo params.json como veja o exemplo:
```
{
    "keywords": "programador",
    "city": "rio janeiro",
    "state": "rj",
    "limit": 1000,
    "profissionalArea": ["ADMINISTRATION", "AGRICULTURE_LIVESTOCK_VETERINARY", "FOOD_GASTRONOMY"],
    "contract": ["CLT", "SELF_EMPLOYED", "SERVICE_PROVIDER"],
    "journey": ["FULL_TIME", "PARTIAL_MORNINGS", "PARTIAL_AFTERNOONS"],
    "pwd": ["HEARING", "SPEECH", "PHYSICAL"],
    "salary": "FROM_TEN_THOUSAND",
    "workplaceType": "ONSITE"
}
```
- keywords: são as palavras-chave que serão usadas para buscar os empregos
- city: é a cidade em que se deseja buscar as vagas e pode ser omitido por exemplo: caso o workplaceType seja remoto. Tome cuidado que algumas cidades tem o nome diferente no infojosbs, por exemplo rio de janeiro é interpretado como: rio janeiro. Então, para saber qual nome usar faça uma busca com a cidade desejada e vá para a página 2 e copie o nome da cidade que aparece na barra de endereços.
- state: é o estado em que se deseja buscar as vagas e é opcional
- limit: é o limite de vagas a serem buscadas e caso seja -1 não é limitado
- profissionalArea: é uma lista com as área profissionais e pode conter um desses valores:
    | Área profissional | Descrição |
    | --- | --- |
    | ADMINISTRATION | Administração |
    | AGRICULTURE_LIVESTOCK_VETERINARY |  Agricultura, Pecuária ou Veterinária |
    | FOOD_GASTRONOMY | Alimentação / Gastronomia |
    | ARCHITECTURE_DECORATION_DESIGN | Arquitetura, Decoração ou Design |
    | ART | Arte |
    | AUDIT | Auditoria |
    | ACCOUNTING_FINANCE_ECONOMICS | Contábil, Finanças ou Economia |
    | CULTURE_LEISURE_ENTERTAINMENT | Cultura, Lazer ou Entretenimento |
    | EDUCATION_TEACHING_LANGUAGES | Educação, Ensino ou Idiomas |
    | ENGINEERING | Engenharia |
    | AESTHETICS | Estética |
    | HOSPITALITY_TOURISM | Hotelaria ou Turismo |
    | FASHION | Moda |
    | QUALITY | Qualidade |
    | CHEMISTRY_PETROCHEMISTRY | Química ou Petroquímica |
    | HUMAN_RESOURCES | Recursos Humanos |
    | HEALTH | Saúde |
    | SECURITY | Segurança |
- contract: é uma lista com os tipos de contratos e pode conter um desses valores:
    | Contrato | Descrição |
    | --- | --- |
    | CLT | CLT |
    | SELF_EMPLOYED | Autônomo |
    | SERVICE_PROVIDER | Prestador de serviços |
    | YOUNG_APPRENTICE | Jovem Aprendiz |
    | INTERNSHIP | Estágio |
    | TEMPORARY | Temporário |
    | TRAINEE | Trainee |
    | OTHERS | Outros |
- journey: é uma lista com os tipos de jornadas e pode conter um desses valores:
    | Jornada | Descrição |
    | --- | --- |
    | FULL_TIME | Período Integral |
    | PARTIAL_MORNINGS | Parcial Manhãs |
    | PARTIAL_AFTERNOONS | Parcial Tardes |
    | PARTIAL_NIGHTS | Parcial Noites |
    | NIGHT | Noturno |
- pwd: é uma lista com deficiências e pode conter um desses valores:
    | Deficiência | Descrição |
    | --- | --- |
    | HEARING | Auditiva |
    | SPEECH | Fala |
    | PHYSICAL | Física |
    | MENTAL | Mental |
    | VISUAL | Visual |
    | PSYCHOSOCIAL | Psicossocial |
    | REHABILITATED | Reabilitados |
- workplaceType: é o modo de trabalho e pode ser um desses seguintes valores:
    | Modo de Trabalho | Descrição |
    | --- | --- |
    | ONSITE | Presencial |
    | REMOTE | Remoto |
    | HYBRID | Híbrido |
- salary: é o salário e pode ser um desses seguintes valores:
    | Salário | Descrição |
    | --- | --- |
    | UP_TO_A_THOUSAND | Até R$ 1000 |
    | FROM_A_THOUSAND | A partir de R$ 1000 |
    | FROM_TWO_THOUSAND | A partir de R$ 2000 |
    | FROM_THREE_THOUSAND | A partir de R$ 3000 |
    | FROM_FOUR_THOUSAND | A partir de R$ 4000 |
    | FROM_FIVE_THOUSAND | A partir de R$ 5000 |
    | FROM_SIX_THOUSAND | A partir de R$ 6000 |
    | FROM_SEVEN_THOUSAND | A partir de R$ 7000 |
    | FROM_EIGHT_THOUSAND | A partir de R$ 8000 |
    | FROM_NIVE_THOUSAND | A partir de R$ 9000 |
    | FROM_TEN_THOUSAND | A partir de R$ 10000 |
    | TO_COMBINE | A combinar |
