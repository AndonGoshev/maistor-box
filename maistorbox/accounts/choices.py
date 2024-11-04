from django.db import models


class UserTypeChoice(models.TextChoices):
    REGULAR_USER = 'regular-user', 'Regular User'
    CONTRACTOR_USER = 'contractor-user', 'Contractor User'


class ContractorRegions(models.TextChoices):
    SOFIA_GRAD = 'Sofia Grad', 'София град'
    PLOVDIV = 'Plovdiv', 'Пловдив'
    VARNA = 'Varna', 'Варна'
    BURGAS = 'Burgas', 'Бургас'
    STARA_ZAGORA = 'Stara Zagora', 'Стара Загора'
    BLAGOEVGRAD = 'Blagoevgrad', 'Благоевград'
    PAZARDZHIK = 'Pazardzhik', 'Пазарджик'
    SOFIA_OBLAST = 'Sofia Oblast', 'София-област'
    PLEVEN = 'Pleven', 'Плевен'
    VELIKO_TARNOVO = 'Veliko Tarnovo', 'Велико Търново'
    HASKOVO = 'Haskovo', 'Хасково'
    RUSE = 'Ruse', 'Русе'
    SLIVEN = 'Sliven', 'Сливен'
    SHUMEN = 'Shumen', 'Шумен'
    DOBRICH = 'Dobrich', 'Добрич'
    KARDJALI = 'Kardzhali', 'Кърджали'
    VRATSA = 'Vratsa', 'Враца'
    MONTANA = 'Montana', 'Монтана'
    LOVEC = 'Lovech', 'Ловеч'
    PERNIK = 'Pernik', 'Перник'
    YAMBOL = 'Yambol', 'Ямбол'
    KYUSTENDIL = 'Kyustendil', 'Кюстендил'
    TARGOVISHTE = 'Targovishte', 'Търговище'
    RAZGRAD = 'Razgrad', 'Разград'
    SILISTRA = 'Silistra', 'Силистра'
    GABROVO = 'Gabrovo', 'Габрово'
    SMOLYAN = 'Smolyan', 'Смолян'
    VIDIN = 'Vidin', 'Видин'