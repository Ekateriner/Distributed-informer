import numpy as np
from sklearn.tree import DecisionTreeRegressor

class TrafficPredictor:
    # TODO: unittests?, 
    # TODO: декоратор проверки аргументов или 
    #       сменить типизацию на статическую через types, 
    # TODO: argparse вместо if-ов
    
    # TODO после появления тестовых данных:
    # TODO: добавить cross-val 
    # TODO: добавить ансамблирование моделей
    # TODO: добавить автоподсчёт метрик качества

    def __init__(self, 
                 seed=42, 
                 value_increments=None,
                 time_steps=None,
                 custom_metrics=None,
                 base_model=DecisionTreeRegressor,
                 **kwargs):
        """
        :param seed: random_seed для случайной инициализации весов
        :param value_increments: ndarray(np.float64) из приращений 
                                 целевой величины
        :param time_steps: ndarray(np.datetime64) из дат измерений
        :param custom_metrics: dict[str : ndarray(np.float64)] - словарь 
                               дополнительных метрик, используемых в качестве 
                               признаков при предсказании
        :param base_model: базовая модель предсказания
        :param **kwargs: гиперпараметры для базовой модели
        """
        self.seed = seed
        self.model = base_model(**kwargs)

        self.value_increments = value_increments
        self.time_steps = time_steps
        self.custom_metrics = custom_metrics
        

    def add(self, new_time_steps, new_value_increments, new_custom_metrics=None):
        """
        Добавляет новые данные
        :param new_increments: ndarray(np.float64) из новых приращений
        :param new_time_steps: ndarray(np.float64) из новых дат измерений
        :param new_custom_metrics: dict[str : ndarray(np.float64)] - словарь новых 
                               дополнительных метрик, используемых в качестве 
                               признаков при предсказании
        """
        if new_value_increments.shape != new_time_steps.shape:
            raise ValueError('Shape mismatch: new_value_increments and new_dates should have the same shape')
        if self.value_increments is None:
            self.value_increments = new_value_increments
        else: 
            self.value_increments = np.append(self.value_increments, 
                                              new_value_increments)
        if self.time_steps is None:
            self.time_steps = new_time_steps
        else:
            self.time_steps = np.append(self.time_steps, new_time_steps)
            
        if self.custom_metrics is None:
            self.custom_metrics = new_custom_metrics
        elif new_custom_metrics is not None:
            for key, values in new_custom_metrics.items():
                if key in self.custom_metrics.keys():
                    self.custom_metrics[key] = np.append(self.custom_metrics[key], values)
                else:
                    self.custom_metrics[key] = values
                    
        self.value_increments = self.value_increments.reshape(-1, 1)
        self.time_steps = self.time_steps.reshape(-1, 1)
        
    
    def get_data(self):
        """
        Возвращает текущие данные класса
        :returns: tuple длины 3 из удаленных self.value_increments,
                  self.time_steps и self.custom_metrics
        """
        return self.value_increments, self.time_steps, self.custom_metrics
    
    def reset_data(self):
        """
        Обнуляет данные класса, не затрагивая модель предсказания
        :returns: tuple длины 3 из удаленных self.value_increments,
                  self.time_steps и self.custom_metrics
        """
        saved = self.get_data()
        self.value_increments = None
        self.time_steps = None
        self.custom_metrics = None
        return saved
        
    def transform(self, ignore_custom=False):
        """
        Обучает модель на внутренних данных, записаных в поля класса
        :param ignore_custom: если True, игнорирует признаки в self.custom_metrics
        """
        if not ignore_custom and self.custom_metrics is not None:
            d = len(self.custom_metrics) + 1
            times = self.time_steps.cumsum()
            n = len(shape)
            
            X = np.zeros(shape=(n, d))
            X[:, 0] = times 
            for i, name, feature in enumerate(self.custom_metrics.items()):
                X[:, i] = feature
        else:
            X = self.time_steps.cumsum().reshape(-1, 1)
        y = self.value_increments.reshape(-1, 1)    
        self.model.fit(X, y)
        
    def add_transform(self, new_time_steps, new_value_increments, 
                      new_custom_metrics=None, ignore_custom=False):
        """
        Добавляет новые данные и обучает модель на внутренних данных, записаных в поля класса
        :param ignore_custom: если True, игнорирует признаки в self.custom_metrics
        """
        self.add(new_time_steps, new_value_increments, new_custom_metrics)
        self.transform(ignore_custom)
        
    def predict(self, mode='extrapolate', residium_time=None,
                seq_len=None, time_steps=None, 
                return_full_seq=True):
        """
        Осуществляет предсказание модели
        :param time_steps: приращения времени для предсказания,
                           обязателен для mode='prediction'
        :param seq_len: кол-во измерений за один цикл расчёта трафика
        :param residium_time: остаток времени до перерасчёта трафика, 
                              обязателен для mode='extrapolate'
        :param mode: 'extrapolate' или 'prediction' - экстраполировать последовательность 
                      или предсказать для следующих шагов time_steps
        :param return_full_seq: если True, возвращает всю последовательность 
                                (train @ pred), иначе - только pred       
        """
        if mode == 'extrapolate':
            if residium_time is None: 
                raise AttributeError('residium_time should be defined in extrapolate mode')
            if seq_len is None: 
                raise AttributeError('seq_len should be defined in extrapolate mode')
            if not isinstance(seq_len, int):
                raise AttributeError('seq_len should be integer in extrapolate mode')
            if seq_len <= len(self.value_increments):
                raise AttributeError('seq_len should be more than sample size in extrapolate mode')
            
            residium_measurements = seq_len - len(self.value_increments)
            last = self.time_steps.cumsum()[-1]
            times = np.linspace(last, 
                                residium_time, 
                                residium_measurements, 
                                endpoint=True)
            pred = self.model.predict(times.reshape(-1, 1))
            if return_full_seq:
                return np.append(self.value_increments, pred)
            return pred
        
        elif mode == 'prediction':
            if time_steps is None:
                raise AttributeError('time_steps should be defined in prediction mode')
            last = self.time_steps.cumsum()[-1]
            times = last + time_steps.cumsum()
            pred = self.model.predict(times.reshape(-1, 1))
            return pred
                
            
    def predict_quantile(self, n, k, residium_time, mode='fraction'):
        """
        Предсказывает квантиль счётчика
        :param n: порядок квантили (либо это доля, либо процент - в зависимости от mode)
        :param k: кол-во измерений
        :param residium_time: остаток времени до перерасчёта трафика
        :param mode: 'fraction' или 'percent' - задаёт способ определения квантили
        """
        pred = self.predict(mode='extrapolate', residium_time=residium_time,
                                seq_len=k, return_full_seq=True)
        if mode == 'fraction':
            return np.quantile(pred.cumsum(), n)
        elif mode == 'percent':
            return np.percentile(pred.cumsum(), n)
        else:
            raise AttributeError('mode should be "fraction" or "percent"')
