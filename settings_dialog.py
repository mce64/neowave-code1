"""دیالوگ تنظیمات"""

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

class SettingsDialog(QDialog):
    """دیالوگ تنظیمات پیشرفته"""
    
    def __init__(self, config, parent=None):
        super().__init__(parent)
        self.config = config
        self.init_ui()
        self.load_current_settings()
        
    def init_ui(self):
        """راه‌اندازی رابط کاربری"""
        self.setWindowTitle("⚙️ تنظیمات پیشرفته")
        self.setMinimumSize(600, 500)
        self.setMaximumSize(800, 600)
        
        layout = QVBoxLayout(self)
        
        # تب‌های تنظیمات
        tabs = QTabWidget()
        
        # تب عمومی
        general_tab = self.create_general_tab()
        tabs.addTab(general_tab, "🏠 عمومی")
        
        # تب تحلیل
        analysis_tab = self.create_analysis_tab()
        tabs.addTab(analysis_tab, "📊 تحلیل")
        
        # تب ظاهر
        appearance_tab = self.create_appearance_tab()
        tabs.addTab(appearance_tab, "🎨 ظاهر")
        
        # تب API
        api_tab = self.create_api_tab()
        tabs.addTab(api_tab, "🔑 API")
        
        layout.addWidget(tabs)
        
        # دکمه‌ها
        buttons_layout = QHBoxLayout()
        
        self.reset_btn = QPushButton("🔄 بازنشانی")
        self.reset_btn.clicked.connect(self.reset_to_defaults)
        
        self.apply_btn = QPushButton("✅ اعمال")
        self.apply_btn.clicked.connect(self.apply_settings)
        
        self.ok_btn = QPushButton("✅ تایید")
        self.ok_btn.clicked.connect(self.accept_settings)
        
        self.cancel_btn = QPushButton("❌ انصراف")
        self.cancel_btn.clicked.connect(self.reject)
        
        buttons_layout.addWidget(self.reset_btn)
        buttons_layout.addStretch()
        buttons_layout.addWidget(self.apply_btn)
        buttons_layout.addWidget(self.ok_btn)
        buttons_layout.addWidget(self.cancel_btn)
        
        layout.addLayout(buttons_layout)
        
    def create_general_tab(self):
        """ایجاد تب تنظیمات عمومی"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # گروه بروزرسانی خودکار
        refresh_group = QGroupBox("🔄 بروزرسانی خودکار")
        refresh_layout = QFormLayout()
        
        self.auto_refresh_check = QCheckBox()
        self.auto_refresh_check.setChecked(True)
        refresh_layout.addRow("فعال‌سازی بروزرسانی خودکار:", self.auto_refresh_check)
        
        self.refresh_interval_spin = QSpinBox()
        self.refresh_interval_spin.setRange(10, 3600)
        self.refresh_interval_spin.setValue(60)
        self.refresh_interval_spin.setSuffix(" ثانیه")
        refresh_layout.addRow("فاصله بروزرسانی:", self.refresh_interval_spin)
        
        refresh_group.setLayout(refresh_layout)
        layout.addWidget(refresh_group)
        
        # گروه ذخیره‌سازی
        save_group = QGroupBox("💾 ذخیره‌سازی")
        save_layout = QFormLayout()
        
        self.auto_save_check = QCheckBox()
        self.auto_save_check.setChecked(True)
        save_layout.addRow("ذخیره خودکار تنظیمات:", self.auto_save_check)
        
        self.backup_data_check = QCheckBox()
        self.backup_data_check.setChecked(False)
        save_layout.addRow("پشتیبان‌گیری از داده‌ها:", self.backup_data_check)
        
        save_group.setLayout(save_layout)
        layout.addWidget(save_group)
        
        # گروه اعلان‌ها
        notifications_group = QGroupBox("🔔 اعلان‌ها")
        notifications_layout = QFormLayout()
        
        self.sound_alerts_check = QCheckBox()
        self.sound_alerts_check.setChecked(True)
        notifications_layout.addRow("هشدارهای صوتی:", self.sound_alerts_check)
        
        self.popup_alerts_check = QCheckBox()
        self.popup_alerts_check.setChecked(True)
        notifications_layout.addRow("پنجره‌های هشدار:", self.popup_alerts_check)
        
        self.email_alerts_check = QCheckBox()
        self.email_alerts_check.setChecked(False)
        notifications_layout.addRow("اعلان‌های ایمیل:", self.email_alerts_check)
        
        notifications_group.setLayout(notifications_layout)
        layout.addWidget(notifications_group)
        
        layout.addStretch()
        return widget
        
    def create_analysis_tab(self):
        """ایجاد تب تنظیمات تحلیل"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # گروه تنظیمات موج شماری
        wave_group = QGroupBox("🌊 موج شماری")
        wave_layout = QFormLayout()
        
        self.pivot_window_spin = QSpinBox()
        self.pivot_window_spin.setRange(3, 20)
        self.pivot_window_spin.setValue(5)
        self.pivot_window_spin.setToolTip("اندازه پنجره برای شناسایی نقاط پیوت")
        wave_layout.addRow("پنجره پیوت:", self.pivot_window_spin)
        
        self.min_wave_size_spin = QSpinBox()
        self.min_wave_size_spin.setRange(5, 100)
        self.min_wave_size_spin.setValue(10)
        self.min_wave_size_spin.setSuffix(" کندل")
        wave_layout.addRow("حداقل اندازه موج:", self.min_wave_size_spin)
        
        self.wave_degree_combo = QComboBox()
        self.wave_degree_combo.addItems(["Minuette", "Minute", "Minor", "Intermediate", "Primary"])
        self.wave_degree_combo.setCurrentText("Minor")
        wave_layout.addRow("درجه موج:", self.wave_degree_combo)
        
        wave_group.setLayout(wave_layout)
        layout.addWidget(wave_group)
        
        # گروه تنظیمات فیبوناچی
        fib_group = QGroupBox("📏 فیبوناچی")
        fib_layout = QFormLayout()
        
        self.fib_precision_spin = QDoubleSpinBox()
        self.fib_precision_spin.setRange(0.1, 10.0)
        self.fib_precision_spin.setValue(2.0)
        self.fib_precision_spin.setSuffix("%")
        self.fib_precision_spin.setDecimals(1)
        fib_layout.addRow("دقت فیبوناچی:", self.fib_precision_spin)
        
        self.fib_levels_edit = QLineEdit()
        self.fib_levels_edit.setText("0.236, 0.382, 0.5, 0.618, 0.786, 1.0")
        self.fib_levels_edit.setToolTip("سطوح فیبوناچی جدا شده با کاما")
        fib_layout.addRow("سطوح فیبوناچی:", self.fib_levels_edit)
        
        self.show_fib_labels_check = QCheckBox()
        self.show_fib_labels_check.setChecked(True)
        fib_layout.addRow("نمایش برچسب‌ها:", self.show_fib_labels_check)
        
        fib_group.setLayout(fib_layout)
        layout.addWidget(fib_group)
        
        # گروه تنظیمات تشخیص الگو
        pattern_group = QGroupBox("🎯 تشخیص الگو")
        pattern_layout = QFormLayout()
        
        self.pattern_sensitivity_slider = QSlider(Qt.Horizontal)
        self.pattern_sensitivity_slider.setRange(1, 10)
        self.pattern_sensitivity_slider.setValue(5)
        self.sensitivity_label = QLabel("متوسط")
        self.pattern_sensitivity_slider.valueChanged.connect(self.update_sensitivity_label)
        sensitivity_layout = QHBoxLayout()
        sensitivity_layout.addWidget(self.pattern_sensitivity_slider)
        sensitivity_layout.addWidget(self.sensitivity_label)
        pattern_layout.addRow("حساسیت تشخیص:", sensitivity_layout)
        
        self.min_pattern_strength_spin = QDoubleSpinBox()
        self.min_pattern_strength_spin.setRange(0.1, 1.0)
        self.min_pattern_strength_spin.setValue(0.7)
        self.min_pattern_strength_spin.setDecimals(2)
        pattern_layout.addRow("حداقل قدرت الگو:", self.min_pattern_strength_spin)
        
        pattern_group.setLayout(pattern_layout)
        layout.addWidget(pattern_group)
        
        layout.addStretch()
        return widget
        
    def create_appearance_tab(self):
        """ایجاد تب تنظیمات ظاهر"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # گروه تم
        theme_group = QGroupBox("🎨 تم و رنگ‌ها")
        theme_layout = QFormLayout()
        
        self.theme_combo = QComboBox()
        self.theme_combo.addItems(["تیره", "روشن", "آبی", "سبز", "بنفش"])
        self.theme_combo.setCurrentText("تیره")
        theme_layout.addRow("تم اصلی:", self.theme_combo)
        
        # رنگ‌های نمودار
        self.bullish_color_btn = QPushButton()
        self.bullish_color_btn.setStyleSheet("background-color: #4CAF50; border: 1px solid black;")
        self.bullish_color_btn.clicked.connect(lambda: self.choose_color(self.bullish_color_btn))
        theme_layout.addRow("رنگ صعودی:", self.bullish_color_btn)
        
        self.bearish_color_btn = QPushButton()
        self.bearish_color_btn.setStyleSheet("background-color: #f44336; border: 1px solid black;")
        self.bearish_color_btn.clicked.connect(lambda: self.choose_color(self.bearish_color_btn))
        theme_layout.addRow("رنگ نزولی:", self.bearish_color_btn)
        
        theme_group.setLayout(theme_layout)
        layout.addWidget(theme_group)
        
        # گروه فونت
        font_group = QGroupBox("🔤 فونت")
        font_layout = QFormLayout()
        
        self.font_family_combo = QComboBox()
        self.font_family_combo.addItems(["Arial", "Tahoma", "Calibri", "Consolas", "Times New Roman"])
        self.font_family_combo.setCurrentText("Tahoma")
        font_layout.addRow("نوع فونت:", self.font_family_combo)
        
        self.font_size_spin = QSpinBox()
        self.font_size_spin.setRange(8, 24)
        self.font_size_spin.setValue(10)
        font_layout.addRow("اندازه فونت:", self.font_size_spin)
        
        self.bold_font_check = QCheckBox()
        self.bold_font_check.setChecked(False)
        font_layout.addRow("فونت ضخیم:", self.bold_font_check)
        
        font_group.setLayout(font_layout)
        layout.addWidget(font_group)
        
        # گروه نمودار
        chart_group = QGroupBox("📊 تنظیمات نمودار")
        chart_layout = QFormLayout()
        
        self.grid_opacity_slider = QSlider(Qt.Horizontal)
        self.grid_opacity_slider.setRange(0, 100)
        self.grid_opacity_slider.setValue(30)
        self.opacity_label = QLabel("30%")
        self.grid_opacity_slider.valueChanged.connect(self.update_opacity_label)
        opacity_layout = QHBoxLayout()
        opacity_layout.addWidget(self.grid_opacity_slider)
        opacity_layout.addWidget(self.opacity_label)
        chart_layout.addRow("شفافیت گرید:", opacity_layout)
        
        self.candle_width_spin = QDoubleSpinBox()
        self.candle_width_spin.setRange(0.1, 2.0)
        self.candle_width_spin.setValue(0.8)
        self.candle_width_spin.setDecimals(1)
        chart_layout.addRow("عرض کندل:", self.candle_width_spin)
        
        chart_group.setLayout(chart_layout)
        layout.addWidget(chart_group)
        
        layout.addStretch()
        return widget
        
    def create_api_tab(self):
        """ایجاد تب تنظیمات API"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # گروه تنظیمات صرافی
        exchange_group = QGroupBox("🏦 تنظیمات صرافی")
        exchange_layout = QFormLayout()
        
        self.exchange_combo = QComboBox()
        self.exchange_combo.addItems(["Binance", "Bybit", "OKX", "KuCoin", "Huobi"])
        self.exchange_combo.setCurrentText("Binance")
        exchange_layout.addRow("صرافی:", self.exchange_combo)
        
        self.sandbox_mode_check = QCheckBox()
        self.sandbox_mode_check.setChecked(True)
        self.sandbox_mode_check.setToolTip("استفاده از حالت تست برای API")
        exchange_layout.addRow("حالت تست (Sandbox):", self.sandbox_mode_check)
        
        exchange_group.setLayout(exchange_layout)
        layout.addWidget(exchange_group)
        
        # گروه محدودیت‌های API
        limits_group = QGroupBox("⚡ محدودیت‌های API")
        limits_layout = QFormLayout()
        
        self.rate_limit_spin = QSpinBox()
        self.rate_limit_spin.setRange(1, 100)
        self.rate_limit_spin.setValue(10)
        self.rate_limit_spin.setSuffix(" درخواست/دقیقه")
        limits_layout.addRow("محدودیت نرخ:", self.rate_limit_spin)
        
        self.timeout_spin = QSpinBox()
        self.timeout_spin.setRange(5, 60)
        self.timeout_spin.setValue(30)
        self.timeout_spin.setSuffix(" ثانیه")
        limits_layout.addRow("تایم‌اوت درخواست:", self.timeout_spin)
        
        self.retry_attempts_spin = QSpinBox()
        self.retry_attempts_spin.setRange(1, 10)
        self.retry_attempts_spin.setValue(3)
        limits_layout.addRow("تعداد تلاش مجدد:", self.retry_attempts_spin)
        
        limits_group.setLayout(limits_layout)
        layout.addWidget(limits_group)
        
        # گروه امنیت
        security_group = QGroupBox("🔒 امنیت")
        security_layout = QFormLayout()
        
        self.encrypt_keys_check = QCheckBox()
        self.encrypt_keys_check.setChecked(True)
        security_layout.addRow("رمزنگاری کلیدها:", self.encrypt_keys_check)
        
        self.log_requests_check = QCheckBox()
        self.log_requests_check.setChecked(False)
        self.log_requests_check.setToolTip("ثبت درخواست‌های API (توجه: ممکن است حساس باشد)")
        security_layout.addRow("ثبت درخواست‌ها:", self.log_requests_check)
        
        security_group.setLayout(security_layout)
        layout.addWidget(security_group)
        
        layout.addStretch()
        return widget
        
    def update_sensitivity_label(self, value):
        """بروزرسانی برچسب حساسیت"""
        sensitivity_levels = {
            1: "خیلی کم", 2: "کم", 3: "کم‌تر از متوسط", 4: "کمی کم", 5: "متوسط",
            6: "کمی زیاد", 7: "بیشتر از متوسط", 8: "زیاد", 9: "خیلی زیاد", 10: "حداکثر"
        }
        self.sensitivity_label.setText(sensitivity_levels.get(value, "متوسط"))
        
    def update_opacity_label(self, value):
        """بروزرسانی برچسب شفافیت"""
        self.opacity_label.setText(f"{value}%")
        
    def choose_color(self, button):
        """انتخاب رنگ"""
        color = QColorDialog.getColor()
        if color.isValid():
            button.setStyleSheet(f"background-color: {color.name()}; border: 1px solid black;")
            
    def load_current_settings(self):
        """بارگذاری تنظیمات فعلی"""
        try:
            # بارگذاری تنظیمات از config object اگر موجود باشد
            if hasattr(self.config, 'analysis'):
                self.auto_refresh_check.setChecked(
                    getattr(self.config.analysis, 'auto_refresh', True)
                )
                self.refresh_interval_spin.setValue(
                    getattr(self.config.analysis, 'refresh_interval', 60)
                )
                
            # در صورت عدم وجود config، تنظیمات پیش‌فرض باقی می‌ماند
        except AttributeError:
            # استفاده از تنظیمات پیش‌فرض
            pass
            
    def apply_settings(self):
        """اعمال تنظیمات بدون بستن دیالوگ"""
        self.save_settings()
        QMessageBox.information(self, "اعمال تنظیمات", "تنظیمات با موفقیت اعمال شد")
        
    def accept_settings(self):
        """تایید و ذخیره تنظیمات"""
        self.save_settings()
        self.accept()
        
    def save_settings(self):
        """ذخیره تنظیمات"""
        try:
            # ذخیره تنظیمات در config object
            settings_data = {
                'auto_refresh': self.auto_refresh_check.isChecked(),
                'refresh_interval': self.refresh_interval_spin.value(),
                'pivot_window': self.pivot_window_spin.value(),
                'fib_precision': self.fib_precision_spin.value(),
                'theme': self.theme_combo.currentText(),
                'font_size': self.font_size_spin.value(),
                'font_family': self.font_family_combo.currentText(),
                'exchange': self.exchange_combo.currentText(),
                'sandbox_mode': self.sandbox_mode_check.isChecked(),
                'rate_limit': self.rate_limit_spin.value(),
                'timeout': self.timeout_spin.value()
            }
            
            # ذخیره در فایل JSON
            import json
            import os
            
            config_dir = "config"
            if not os.path.exists(config_dir):
                os.makedirs(config_dir)
                
            config_file = os.path.join(config_dir, "settings.json")
            with open(config_file, 'w', encoding='utf-8') as f:
                json.dump(settings_data, f, ensure_ascii=False, indent=2)
                
        except Exception as e:
            QMessageBox.warning(self, "خطا", f"خطا در ذخیره تنظیمات: {str(e)}")
            
    def reset_to_defaults(self):
        """بازنشانی به تنظیمات پیش‌فرض"""
        reply = QMessageBox.question(
            self, "بازنشانی تنظیمات",
            "آیا مطمئن هستید که می‌خواهید تمام تنظیمات را به حالت پیش‌فرض بازگردانید؟",
            QMessageBox.Yes | QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            # بازنشانی تب عمومی
            self.auto_refresh_check.setChecked(True)
            self.refresh_interval_spin.setValue(60)
            self.auto_save_check.setChecked(True)
            self.backup_data_check.setChecked(False)
            self.sound_alerts_check.setChecked(True)
            self.popup_alerts_check.setChecked(True)
            self.email_alerts_check.setChecked(False)
            
            # بازنشانی تب تحلیل
            self.pivot_window_spin.setValue(5)
            self.min_wave_size_spin.setValue(10)
            self.wave_degree_combo.setCurrentText("Minor")
            self.fib_precision_spin.setValue(2.0)
            self.fib_levels_edit.setText("0.236, 0.382, 0.5, 0.618, 0.786, 1.0")
            self.show_fib_labels_check.setChecked(True)
            self.pattern_sensitivity_slider.setValue(5)
            self.min_pattern_strength_spin.setValue(0.7)
            
            # بازنشانی تب ظاهر
            self.theme_combo.setCurrentText("تیره")
            self.font_family_combo.setCurrentText("Tahoma")
            self.font_size_spin.setValue(10)
            self.bold_font_check.setChecked(False)
            self.grid_opacity_slider.setValue(30)
            self.candle_width_spin.setValue(0.8)
            
            # بازنشانی تب API
            self.exchange_combo.setCurrentText("Binance")
            self.sandbox_mode_check.setChecked(True)
            self.rate_limit_spin.setValue(10)
            self.timeout_spin.setValue(30)
            self.retry_attempts_spin.setValue(3)
            self.encrypt_keys_check.setChecked(True)
            self.log_requests_check.setChecked(False)
            
            QMessageBox.information(self, "بازنشانی", "تنظیمات به حالت پیش‌فرض بازگردانده شد")