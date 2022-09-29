from dataclasses import dataclass, asdict, fields
from typing import Dict, Any


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""

    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float

    MESSAGE: str = ('Тип тренировки: {training_type}; '
                    'Длительность: {duration:.3f} ч.; '
                    'Дистанция: {distance:.3f} км; '
                    'Ср. скорость: {speed:.3f} км/ч; '
                    'Потрачено ккал: {calories:.3f}.')

    def get_message(self) -> str:
        return self.MESSAGE.format(**asdict(self))


@dataclass
class Training:
    """Базовый класс тренировки."""

    LEN_STEP = 0.65
    M_IN_KM = 1000
    M_IN_H = 60

    action: int
    duration: float
    weight: float

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        training_mean_speed = self.get_distance() / self.duration
        return training_mean_speed

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        raise NotImplementedError('Определите get_spent_calories в %s'
                                  % type(self).__name__)

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(type(self).__name__, self.duration,
                           self.get_distance(), self.get_mean_speed(),
                           self.get_spent_calories())


@dataclass
class Running(Training):
    """Тренировка: бег."""

    COEFF_MEAN_SPEED_1 = 18
    COEFF_MEAN_SPEED_2 = 20

    def get_spent_calories(self) -> float:
        return ((self.COEFF_MEAN_SPEED_1 * self.get_mean_speed()
                 - self.COEFF_MEAN_SPEED_2)
                * self.weight / self.M_IN_KM
                * self.duration * self.M_IN_H)


@dataclass
class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""

    COEFF_WEIGHT_1 = 0.035
    COEFF_WEIGHT_2 = 0.029
    EXPONENT = 2

    action: int
    duration: float
    weight: float
    height: float

    def get_spent_calories(self) -> float:
        return (
            (self.COEFF_WEIGHT_1 * self.weight
             + (self.get_mean_speed() ** self.EXPONENT
                // self.weight)
             * self.COEFF_WEIGHT_2 * self.weight)
            * self.duration * self.M_IN_H)


@dataclass
class Swimming(Training):
    """Тренировка: плавание."""

    LEN_STEP = 1.38
    COEFF_MEAN_SPEED = 1.1
    COEFF_WEIGHT = 2

    action: int
    duration: float
    weight: float
    length_pool: float
    count_pool: int

    def get_mean_speed(self) -> float:
        return (self.length_pool * self.count_pool / self.M_IN_KM
                / self.duration)

    def get_spent_calories(self) -> float:
        return ((self.get_mean_speed() + self.COEFF_MEAN_SPEED)
                * self.COEFF_WEIGHT * self.weight)


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    training_type: Dict[str, Any] = {
        'SWM': (Swimming, len(fields(Swimming))),
        'RUN': (Running, len(fields(Running))),
        'WLK': (SportsWalking, len(fields(SportsWalking)))
    }
    if workout_type not in training_type:
        raise KeyError(f'кода тренировки {workout_type} нет в списке')
    if training_type[workout_type][1] != len(data):
        raise ValueError(f'недопустимое количество значений. '
                         f'Пришло значений: {len(data)}, '
                         f'ожидается: {training_type[workout_type][1]}')
    return training_type[workout_type][0](*data)


def main(training: Training) -> None:
    """Главная функция."""
    print(training.show_training_info().get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180])
    ]

    for workout_type, data in packages:
        main(read_package(workout_type, data))
